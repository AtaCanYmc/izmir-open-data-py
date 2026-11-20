import pytest
import respx
from httpx import Response

from izmir_open_data import CKANQueryBuilder, IzmirClient


def test_ckan_query_builder_params():
    client = IzmirClient()
    builder = (
        CKANQueryBuilder(client, "test-res")
        .where("ILCE", "KONAK")
        .where("DURUM", "AKTIF")
        .search("Alsancak")
        .page(2, 25)
        .sort("TARIH", "desc")
        .fields(["ID", "ADI", "KONUM"])
    )

    params = builder.to_params()
    assert params["resource_id"] == "test-res"
    assert params["q"] == "Alsancak"
    assert params["filters"] == {"ILCE": "KONAK", "DURUM": "AKTIF"}
    assert params["limit"] == 25
    assert params["offset"] == 25
    assert params["sort"] == "TARIH desc"
    assert params["fields"] == ["ID", "ADI", "KONUM"]


@pytest.mark.asyncio
@respx.mock
async def test_ckan_query_execute():
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "result": {
                    "resource_id": "res-123",
                    "total": 1,
                    "records": [{"_id": 1, "title": "Park"}],
                },
            },
        )
    )

    client = IzmirClient()
    builder = client.ckan.query("res-123").filter("MAHALLE", "GÖZTEPE").limit(10)
    result = await builder.execute()

    assert result["records"] == [{"_id": 1, "title": "Park"}]
    assert result["total"] == 1
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_ckan_query_fetch_all():
    call_count = 0

    def datastore_side_effect(request):
        nonlocal call_count
        call_count += 1
        offset = request.url.params.get("offset")
        if offset == "0":
            return Response(
                200,
                json={
                    "success": True,
                    "result": {
                        "total": 3,
                        "records": [{"id": 1}, {"id": 2}],
                    },
                },
            )
        return Response(
            200,
            json={
                "success": True,
                "result": {
                    "total": 3,
                    "records": [{"id": 3}],
                },
            },
        )

    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        side_effect=datastore_side_effect
    )

    client = IzmirClient()
    records = await client.ckan.query("res-all").fetch_all(batch_size=2, max_records=10)
    assert len(records) == 3
    assert records == [{"id": 1}, {"id": 2}, {"id": 3}]
    assert call_count == 2
    await client.close()


@pytest.mark.asyncio
@respx.mock
async def test_ckan_endpoint_methods():
    respx.get("https://acikveri.bizizmir.com/api/3/action/package_search").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "result": {"count": 1, "results": [{"name": "pkg1"}]},
            },
        )
    )
    respx.get("https://acikveri.bizizmir.com/api/3/action/package_show").mock(
        return_value=Response(
            200, json={"success": True, "result": {"id": "pkg1", "title": "Package 1"}}
        )
    )
    respx.get("https://acikveri.bizizmir.com/api/3/action/package_list").mock(
        return_value=Response(200, json={"success": True, "result": ["pkg1", "pkg2"]})
    )

    client = IzmirClient()
    search_res = await client.ckan.search_packages("otopark")
    assert search_res["count"] == 1

    pkg = await client.ckan.get_package("pkg1")
    assert pkg["title"] == "Package 1"

    pkgs = await client.ckan.list_packages()
    assert pkgs == ["pkg1", "pkg2"]
    await client.close()
