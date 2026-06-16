import pytest

from izmir_open_data.core.client import IzmirClient


@pytest.mark.asyncio
async def test_client_initialization() -> None:
    client = IzmirClient()
    # Ensure that endpoints are initialized
    assert hasattr(client, "afetler")
    assert hasattr(client, "eshot")
    assert client._client.timeout.read == 30.0
    await client.close()
