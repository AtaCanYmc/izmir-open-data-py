import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient


@pytest.mark.asyncio
@respx.mock
async def test_itfaiye_endpoint():
    respx.get("https://openapi.izmir.bel.tr/api/ibb/cbs/itfaiyegruplari").mock(
        return_value=Response(200, json={"onemliyer": [{"Adi": "Konak İtfaiye"}]})
    )
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200, json={"success": True, "result": {"records": [{"_id": 1}]}}
        )
    )
    respx.get(
        "https://acikveri.bizizmir.com/datastore/dump/4b7a8da1-94ed-487f-8b7a-e13d40a5cd33?format=json"
    ).mock(return_value=Response(200, json=[{"_id": 1}]))

    client = IzmirClient()
    gruplar = await client.itfaiye.get_gruplar()
    assert "onemliyer" in gruplar

    mudahale = await client.itfaiye.get_acil_mudahale_istatistigi(q="Yangın")
    assert len(mudahale["records"]) == 1

    dump_data = await client.itfaiye.dump_acil_mudahale()
    assert dump_data == [{"_id": 1}]
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_izum_endpoint():
    respx.get("https://openapi.izmir.bel.tr/api/ibb/izum/otoparklar").mock(
        return_value=Response(200, json=[{"id": 1, "adi": "Alsancak Otopark"}])
    )
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200, json={"success": True, "result": {"records": [{"HIZ": 45}]}}
        )
    )

    client = IzmirClient()
    otoparklar = await client.izum.get_otoparklar()
    assert len(otoparklar) == 1
    assert otoparklar[0]["adi"] == "Alsancak Otopark"

    hiz = await client.izum.get_ana_arter_hiz_ve_sure()
    assert hiz["records"][0]["HIZ"] == 45
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_turuncucember_endpoint():
    respx.get("https://openapi.izmir.bel.tr/api/ibb/turuncucember/isletmeler").mock(
        return_value=Response(200, json=[{"Id": 10, "TicariUnvan": "Kafe"}])
    )
    respx.get("https://openapi.izmir.bel.tr/api/ibb/turuncucember/isletme/10").mock(
        return_value=Response(200, json={"Id": 10, "TicariUnvan": "Kafe"})
    )
    respx.get("https://openapi.izmir.bel.tr/api/ibb/turuncucember/sayilar").mock(
        return_value=Response(200, json={"BasvuruSayisi": 150})
    )

    client = IzmirClient()
    isletmeler = await client.turuncucember.get_isletmeler()
    assert len(isletmeler) == 1

    detay = await client.turuncucember.get_isletme(10)
    assert detay["Id"] == 10

    sayilar = await client.turuncucember.get_sayilar()
    assert sayilar["BasvuruSayisi"] == 150
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_tuvalet_endpoint():
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "result": {"records": [{"TESIS_ADI": "Alsancak Tuvalet"}]},
            },
        )
    )

    client = IzmirClient()
    akilli = await client.tuvalet.get_akilli_tuvaletler(q="Alsancak")
    assert akilli["records"][0]["TESIS_ADI"] == "Alsancak Tuvalet"

    moduler = await client.tuvalet.get_moduler_tuvaletler()
    assert len(moduler["records"]) == 1
    await client.close()
