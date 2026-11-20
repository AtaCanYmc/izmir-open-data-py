import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient
from izmir_open_data.mcp import call_endpoint, get_dataset


@pytest.mark.asyncio
async def test_path_traversal_protection():
    client = IzmirClient()
    with pytest.raises(ValueError, match="Geçersiz veya güvensiz istek yolu"):
        await client.get("../../../etc/passwd")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz istek yolu"):
        await client.get("%2e%2e/%2e%2e/etc/passwd")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz istek yolu"):
        await client.get("https://malicious-server.com/api")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz CKAN aksiyonu"):
        await client.get_ckan("../../escape_action")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz CKAN aksiyonu"):
        await client.get_ckan("%2e%2e/escape_action")

    await client.close()


@pytest.mark.asyncio
async def test_csv_scheme_protection():
    client = IzmirClient()
    with pytest.raises(ValueError, match="CSV istekleri yalnızca HTTP veya HTTPS"):
        await client.get_csv("file:///etc/passwd")

    with pytest.raises(ValueError, match="CSV istekleri yalnızca HTTP veya HTTPS"):
        await client.get_csv("ftp://malicious.com/data.csv")

    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_ckan_dump_url_encoding():
    route = respx.get(
        "https://acikveri.bizizmir.com/datastore/dump/res-id%2Fwith%2Fslash?format=json"
    ).mock(return_value=Response(200, json={"data": []}))

    client = IzmirClient()
    await client.get_ckan_dump("res-id/with/slash")
    assert route.called
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_csv_prototype_pollution_protection():
    malicious_csv = """__proto__;constructor;prototype;HAT_NO;HAT_ADI
{"polluted":true};malicious;malicious;5;NARLIDERE
"""
    respx.get("https://test.com/malicious.csv").mock(
        return_value=Response(200, text=malicious_csv)
    )

    client = IzmirClient()
    results = await client.get_csv("https://test.com/malicious.csv")

    assert len(results) == 1
    assert results[0]["HAT_NO"] == 5
    assert results[0]["HAT_ADI"] == "NARLIDERE"
    assert "__proto__" not in results[0]
    assert "constructor" not in results[0]
    assert "prototype" not in results[0]
    await client.close()


def test_ckan_query_builder_sort_sanitization():
    client = IzmirClient()
    query = client.ckan.query("test-id")
    with pytest.raises(ValueError, match="Geçersiz alan adı formatı"):
        query.sort("field; DROP TABLE students;--", "desc")

    query.sort("_id", "DESC")
    params = query.to_params()
    assert params["sort"] == "_id desc"


@pytest.mark.asyncio
async def test_mcp_security_validations():
    with pytest.raises(ValueError, match="Geçersiz veya güvensiz dataset_id formatı"):
        await get_dataset("../../etc/passwd")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz dataset_id formatı"):
        await get_dataset("%2e%2e/passwd")

    res = await call_endpoint("close", "anything")
    assert "Unauthorized or invalid namespace" in res

    res2 = await call_endpoint("cache", "get")
    assert "Unauthorized or invalid namespace" in res2

    res3 = await call_endpoint("nonexistent", "method")
    assert "not found" in res3
