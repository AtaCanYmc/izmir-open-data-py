import pandas as pd
import polars as pl
import pytest
import respx
from httpx import Response
from pydantic import BaseModel

from izmir_open_data import (
    IzmirClient,
    normalize_records,
    to_dataframe,
    to_polars,
)


class DummyModel(BaseModel):
    id: int
    name: str


def test_normalize_records():
    assert normalize_records(None) == []
    assert normalize_records([{"a": 1}]) == [{"a": 1}]
    assert normalize_records({"records": [{"a": 1}]}) == [{"a": 1}]
    assert normalize_records({"kayitlar": [{"a": 2}]}) == [{"a": 2}]
    assert normalize_records({"onemliyer": [{"a": 3}]}) == [{"a": 3}]

    # Pydantic model
    m = DummyModel(id=10, name="Alsancak")
    assert normalize_records([m]) == [{"id": 10, "name": "Alsancak"}]


def test_to_dataframe():
    data = [
        {"id": 1, "station": "Konak", "capacity": 20},
        {"id": 2, "station": "Göztepe", "capacity": 25},
    ]
    df = to_dataframe(data)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df["station"]) == ["Konak", "Göztepe"]
    assert list(df["capacity"]) == [20, 25]


def test_to_polars():
    data = [
        {"id": 1, "station": "Konak", "capacity": 20},
        {"id": 2, "station": "Göztepe", "capacity": 25},
    ]
    pldf = to_polars(data)
    assert isinstance(pldf, pl.DataFrame)
    assert pldf.shape == (2, 3)
    assert pldf["station"].to_list() == ["Konak", "Göztepe"]

    empty_df = to_polars([])
    assert isinstance(empty_df, pl.DataFrame)
    assert len(empty_df) == 0


@pytest.mark.asyncio
@respx.mock
async def test_ckan_query_dataframe_and_polars():
    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "result": {
                    "resource_id": "res-df",
                    "total": 2,
                    "records": [
                        {"_id": 1, "ILCE": "KONAK", "DURUM": "AKTIF"},
                        {"_id": 2, "ILCE": "KARSIYAKA", "DURUM": "PASIF"},
                    ],
                },
            },
        )
    )

    client = IzmirClient()
    df = await client.ckan.query("res-df").to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df["ILCE"]) == ["KONAK", "KARSIYAKA"]

    pldf = await client.ckan.query("res-df").to_polars()
    assert isinstance(pldf, pl.DataFrame)
    assert len(pldf) == 2
    assert pldf["ILCE"].to_list() == ["KONAK", "KARSIYAKA"]

    await client.close()
