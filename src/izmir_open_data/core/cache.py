import time
from typing import Any, Protocol


class CacheProvider(Protocol):
    """Protocol for cache providers."""

    async def get(self, key: str) -> Any | None: ...
    async def set(self, key: str, value: Any, ttl_ms: int | None = None) -> None: ...
    async def delete(self, key: str) -> bool: ...
    async def clear(self) -> None: ...
    async def has(self, key: str) -> bool: ...


class CacheEntry:
    __slots__ = ("value", "expires_at")

    def __init__(self, value: Any, expires_at: float):
        self.value = value
        self.expires_at = expires_at


class MemoryCache:
    """In-memory TTL cache with FIFO eviction."""

    def __init__(self, default_ttl_ms: int = 300_000, max_items: int = 500):
        self.default_ttl_ms = default_ttl_ms if default_ttl_ms > 0 else 300_000
        self.max_items = max_items if max_items > 0 else 500
        self._cache: dict[str, CacheEntry] = {}

    def _now_ms(self) -> float:
        return time.time() * 1000

    async def get(self, key: str) -> Any | None:
        entry = self._cache.get(key)
        if entry is None:
            return None

        if self._now_ms() > entry.expires_at:
            self._cache.pop(key, None)
            return None

        return entry.value

    async def set(self, key: str, value: Any, ttl_ms: int | None = None) -> None:
        ttl = ttl_ms if (ttl_ms is not None and ttl_ms > 0) else self.default_ttl_ms
        expires_at = self._now_ms() + ttl

        # FIFO eviction when capacity is reached and key is new
        if len(self._cache) >= self.max_items and key not in self._cache:
            oldest_key = next(iter(self._cache))
            self._cache.pop(oldest_key, None)

        self._cache[key] = CacheEntry(value=value, expires_at=expires_at)

    async def delete(self, key: str) -> bool:
        return self._cache.pop(key, None) is not None

    async def clear(self) -> None:
        self._cache.clear()

    async def has(self, key: str) -> bool:
        return (await self.get(key)) is not None

    def size(self) -> int:
        now = self._now_ms()
        expired = [k for k, v in self._cache.items() if now > v.expires_at]
        for k in expired:
            self._cache.pop(k, None)
        return len(self._cache)
