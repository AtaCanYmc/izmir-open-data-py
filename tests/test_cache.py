import asyncio

import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient, MemoryCache


@pytest.mark.asyncio
async def test_memory_cache_set_and_get():
    cache = MemoryCache(default_ttl_ms=1000)
    await cache.set("k1", {"name": "Konak"})

    assert await cache.has("k1") is True
    assert await cache.get("k1") == {"name": "Konak"}
    assert cache.size() == 1


@pytest.mark.asyncio
async def test_memory_cache_expiry():
    cache = MemoryCache()
    await cache.set("exp_key", "val", ttl_ms=20)
    assert await cache.get("exp_key") == "val"

    await asyncio.sleep(0.035)
    assert await cache.get("exp_key") is None
    assert await cache.has("exp_key") is False


@pytest.mark.asyncio
async def test_memory_cache_fifo_eviction():
    cache = MemoryCache(max_items=2, default_ttl_ms=10000)
    await cache.set("k1", 1)
    await cache.set("k2", 2)
    await cache.set("k3", 3)

    assert cache.size() == 2
    assert await cache.get("k1") is None
    assert await cache.get("k2") == 2
    assert await cache.get("k3") == 3


@pytest.mark.asyncio
async def test_memory_cache_delete_and_clear():
    cache = MemoryCache()
    await cache.set("a", 1)
    await cache.set("b", 2)

    assert await cache.delete("a") is True
    assert await cache.get("a") is None
    assert cache.size() == 1

    await cache.clear()
    assert cache.size() == 0


@pytest.mark.asyncio
@respx.mock
async def test_client_cache_prevents_duplicate_requests():
    mock_route = respx.get("https://openapi.izmir.bel.tr/api/test_data").mock(
        return_value=Response(200, json=[{"id": 1, "name": "Alsancak"}])
    )

    client = IzmirClient(cache=True)
    res1 = await client.get("test_data")
    res2 = await client.get("test_data")

    assert res1 == [{"id": 1, "name": "Alsancak"}]
    assert res2 == [{"id": 1, "name": "Alsancak"}]
    assert mock_route.call_count == 1

    await client.clear_cache()
    await client.get("test_data")
    assert mock_route.call_count == 2
    await client.close()
