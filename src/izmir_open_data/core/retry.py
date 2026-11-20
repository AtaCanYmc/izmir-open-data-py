import asyncio
import random
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetryConfig:
    retries: int = 3
    base_delay_ms: int = 300
    max_delay_ms: int = 3000
    status_codes: list[int] = field(
        default_factory=lambda: [408, 429, 500, 502, 503, 504]
    )
    jitter: bool = True


DEFAULT_RETRY_CONFIG = RetryConfig()


def calculate_backoff(attempt: int, config: RetryConfig) -> int:
    """Calculate exponential backoff in milliseconds with optional full jitter."""
    safe_attempt = max(1, min(20, attempt))
    base_delay = max(0, config.base_delay_ms)
    max_delay = max(base_delay, config.max_delay_ms)
    exponential = min(max_delay, base_delay * (2 ** (safe_attempt - 1)))

    if not config.jitter:
        return exponential
    return random.randint(0, int(exponential))


def is_retryable_error(error: Any, retry_status_codes: list[int]) -> bool:
    if not error:
        return False

    status = getattr(error, "status_code", getattr(error, "status", None))
    if status is not None and status in retry_status_codes:
        return True

    msg = str(error)
    for code in retry_status_codes:
        if str(code) in msg:
            return True

    transient_phrases = [
        "network",
        "timeout",
        "econnreset",
        "econnrefused",
        "etimedout",
        "connecterror",
        "readtimeout",
        "pooltimeout",
    ]
    lower_msg = msg.lower()
    return any(p in lower_msg for p in transient_phrases)


async def execute_with_retry(
    operation: Callable[[], Coroutine[Any, Any, Any]],
    custom_config: RetryConfig | bool | None = None,
) -> Any:
    if custom_config is False:
        return await operation()

    config = (
        custom_config
        if isinstance(custom_config, RetryConfig)
        else DEFAULT_RETRY_CONFIG
    )
    max_retries = max(0, min(10, config.retries))
    if max_retries <= 0:
        return await operation()

    last_error: Exception | None = None
    for attempt in range(1, max_retries + 2):
        try:
            return await operation()
        except Exception as error:
            last_error = error
            if attempt > max_retries or not is_retryable_error(
                error, config.status_codes
            ):
                raise error

            delay_ms = calculate_backoff(attempt, config)
            if delay_ms > 0:
                await asyncio.sleep(delay_ms / 1000.0)

    if last_error is not None:
        raise last_error
