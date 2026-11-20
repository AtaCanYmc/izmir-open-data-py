import json

import pyarrow.parquet as pq
import pytest
import respx
from httpx import Response

from izmir_open_data import (
    IzmirClient,
    read_parquet,
    to_geoparquet,
    to_parquet,
)


def test_parquet_read_write(tmp_path):
    file_path = tmp_path / "test.parquet"
    data = [
        {"id": 1, "adi": "Kültürpark", "kapasite": 100},
        {"id": 2, "adi": "Fuar", "kapasite": 200},
    ]

    to_parquet(data, file_path)
    assert file_path.exists()

    records = read_parquet(file_path)
    assert len(records) == 2
    assert records[0]["adi"] == "Kültürpark"
    assert records[1]["kapasite"] == 200


def test_geoparquet_metadata_and_geometry(tmp_path):
    file_path = tmp_path / "test.geoparquet"
    data = [
        {
            "Id": 1,
            "Adi": "Konak Meydanı",
            "BOYLAM": 27.1287,
            "ENLEM": 38.4189,
        },
        {
            "Id": 2,
            "Adi": "Gündoğdu Meydanı",
            "BOYLAM": 27.1402,
            "ENLEM": 38.4347,
        },
        {
            "Id": 3,
            "Adi": "Koordinatsız Nokta",
        },
    ]

    to_geoparquet(data, file_path)
    assert file_path.exists()

    # Verify GeoParquet metadata in Parquet schema
    table = pq.read_table(str(file_path))
    assert b"geo" in table.schema.metadata

    geo_meta = json.loads(table.schema.metadata[b"geo"].decode("utf-8"))
    assert geo_meta["version"] == "1.1.0"
    assert geo_meta["primary_column"] == "geometry"
    assert "geometry" in geo_meta["columns"]
    assert geo_meta["columns"]["geometry"]["encoding"] == "WKB"
    assert geo_meta["columns"]["geometry"]["geometry_types"] == ["Point"]

    # Verify WKB geometry column
    records = table.to_pylist()
    assert len(records) == 3
    assert records[0]["geometry"] is not None
    assert len(records[0]["geometry"]) == 21  # 21-byte WKB point
    assert records[2]["geometry"] is None


@pytest.mark.asyncio
@respx.mock
async def test_ckan_query_to_parquet_and_geoparquet(tmp_path):
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "result": {
                    "resource_id": "res-pq",
                    "total": 1,
                    "records": [
                        {
                            "_id": 1,
                            "TESIS_ADI": "Akıllı Tuvalet",
                            "BOYLAM": 27.14,
                            "ENLEM": 38.43,
                        }
                    ],
                },
            },
        )
    )

    client = IzmirClient()
    pq_path = tmp_path / "out.parquet"
    await client.ckan.query("res-pq").to_parquet(pq_path)
    assert pq_path.exists()

    gpq_path = tmp_path / "out.geoparquet"
    await client.ckan.query("res-pq").to_geoparquet(gpq_path)
    assert gpq_path.exists()

    await client.close()
