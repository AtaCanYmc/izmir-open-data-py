import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient


@pytest.mark.asyncio
async def test_path_traversal_protection():
    client = IzmirClient()
    with pytest.raises(ValueError, match="Geçersiz veya güvensiz istek yolu"):
        await client.get("../../../etc/passwd")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz istek yolu"):
        await client.get("https://malicious-server.com/api")

    with pytest.raises(ValueError, match="Geçersiz veya güvensiz CKAN aksiyonu"):
        await client.get_ckan("../../escape_action")

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
