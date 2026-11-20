import pytest
import respx
from httpx import Response

from izmir_open_data import IzmirClient, stream_batches, stream_records


@pytest.mark.asyncio
async def test_stream_batches_and_records():
    # Simulated pager returning 3 items per page up to 8 total
    items = list(range(1, 9))

    async def mock_fetch(offset: int, limit: int) -> list[int]:
        return items[offset : offset + limit]

    batches = []
    async for batch in stream_batches(mock_fetch, batch_size=3):
        batches.append(batch)

    assert batches == [[1, 2, 3], [4, 5, 6], [7, 8]]

    records = []
    async for rec in stream_records(mock_fetch, batch_size=3):
        records.append(rec)

    assert records == [1, 2, 3, 4, 5, 6, 7, 8]


@pytest.mark.asyncio
async def test_stream_max_records():
    items = list(range(1, 20))

    async def mock_fetch(offset: int, limit: int) -> list[int]:
        return items[offset : offset + limit]

    records = []
    async for rec in stream_records(mock_fetch, batch_size=4, max_records=7):
        records.append(rec)

    assert records == [1, 2, 3, 4, 5, 6, 7]


@pytest.mark.asyncio
@respx.mock
async def test_ckan_query_stream():
    call_offsets = []

    def datastore_handler(request):
        offset = int(request.url.params.get("offset", 0))
        call_offsets.append(offset)
        if offset == 0:
            return Response(
                200,
                json={
                    "success": True,
                    "result": {
                        "total": 3,
                        "records": [{"_id": 1}, {"_id": 2}],
                    },
                },
            )
        return Response(
            200,
            json={
                "success": True,
                "result": {
                    "total": 3,
                    "records": [{"_id": 3}],
                },
            },
        )

    respx.get("https://acikveri.bizizmir.com/api/3/action/datastore_search").mock(
        side_effect=datastore_handler
    )

    client = IzmirClient()
    streamed_records = []
    async for record in client.ckan.query("res-stream").stream(batch_size=2):
        streamed_records.append(record)

    assert len(streamed_records) == 3
    assert [r["_id"] for r in streamed_records] == [1, 2, 3]
    assert call_offsets == [0, 2]

    await client.close()
