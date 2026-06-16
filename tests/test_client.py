import pytest
from izmir_open_data.core.client import IzmirClient


@pytest.mark.asyncio
async def test_client_initialization():
    client = IzmirClient()
    assert client.BASE_URL == "https://openapi.izmir.bel.tr/api"
    await client.close()
