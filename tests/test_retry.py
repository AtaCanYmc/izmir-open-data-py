import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient, RetryConfig, execute_with_retry
from izmir_open_data.core.exceptions import APIError
from izmir_open_data.core.retry import calculate_backoff, is_retryable_error


def test_calculate_backoff():
    config = RetryConfig(
        retries=3,
        base_delay_ms=100,
        max_delay_ms=500,
        jitter=False,
    )
    assert calculate_backoff(1, config) == 100
    assert calculate_backoff(2, config) == 200
    assert calculate_backoff(3, config) == 400
    assert calculate_backoff(4, config) == 500

    config_jitter = RetryConfig(
        retries=3,
        base_delay_ms=100,
        max_delay_ms=500,
        jitter=True,
    )
    jitter_val = calculate_backoff(2, config_jitter)
    assert 0 <= jitter_val <= 200


def test_is_retryable_error():
    status_codes = [408, 429, 500, 502, 503, 504]
    err503 = APIError("API response error: 503", status_code=503)
    assert is_retryable_error(err503, status_codes) is True

    err_network = Exception("ConnectError: connection reset")
    assert is_retryable_error(err_network, status_codes) is True

    err404 = APIError("API response error: 404", status_code=404)
    assert is_retryable_error(err404, status_codes) is False
    assert is_retryable_error(None, status_codes) is False


@pytest.mark.asyncio
async def test_execute_with_retry_success():
    calls = 0

    async def _op():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise APIError("API response error: 500", status_code=500)
        return {"success": True}

    res = await execute_with_retry(
        _op,
        RetryConfig(retries=3, base_delay_ms=5, max_delay_ms=20, jitter=False),
    )
    assert res == {"success": True}
    assert calls == 3


@pytest.mark.asyncio
async def test_execute_with_retry_non_retryable():
    calls = 0

    async def _op():
        nonlocal calls
        calls += 1
        raise APIError("API response error: 404", status_code=404)

    with pytest.raises(APIError):
        await execute_with_retry(
            _op,
            RetryConfig(retries=3, base_delay_ms=5),
        )
    assert calls == 1


@pytest.mark.asyncio
@respx.mock
async def test_client_retry_integration():
    respx.get("https://openapi.izmir.bel.tr/api/flaky").mock(
        side_effect=[
            Response(502),
            Response(200, json={"ok": True}),
        ]
    )

    client = IzmirClient(retry=RetryConfig(retries=2, base_delay_ms=5, max_delay_ms=20))
    result = await client.get("flaky")
    assert result == {"ok": True}
    await client.close()
