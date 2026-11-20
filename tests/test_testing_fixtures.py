import pytest

from izmir_open_data import MockIzmirClient, get_fixture


def test_get_fixture():
    eczaneler = get_fixture("eczaneler")
    assert isinstance(eczaneler, list)
    assert len(eczaneler) >= 2
    assert eczaneler[0]["Ilce"] == "KONAK"

    with pytest.raises(KeyError, match="Bilinmeyen test verisi"):
        get_fixture("non_existent_fixture")


@pytest.mark.asyncio
async def test_mock_client_offline_requests():
    client = MockIzmirClient()

    # REST endpoint call via MockIzmirClient
    eczaneler = await client.eczaneler.get_list()
    assert len(eczaneler) >= 2
    assert eczaneler[0]["Adi"] == "Alsancak Eczanesi"

    # BISIM endpoint call via MockIzmirClient
    bisim = await client.bisim.get_istasyon_list()
    assert len(bisim["kayitlar"]) >= 2
    assert bisim["kayitlar"][0]["adi"] == "Alsancak İskele"

    # CKAN Datastore call via MockIzmirClient
    tuvaletler = await client.tuvalet.get_akilli_tuvaletler()
    assert len(tuvaletler["records"]) >= 2
    assert tuvaletler["records"][0]["TESIS_ADI"] == "Kordon Akıllı Tuvalet"

    # ESHOT CSV call via MockIzmirClient
    hatlar = await client.eshot.get_hatlar()
    assert len(hatlar) >= 2
    assert hatlar[0]["HAT_NO"] == 5

    # Check call recorder
    assert len(client.recorded_calls) >= 4
    await client.close()


@pytest.mark.asyncio
async def test_mock_client_error_simulation():
    client = MockIzmirClient(simulate_error=ConnectionError("Ağ bağlantısı yok"))
    with pytest.raises(ConnectionError, match="Ağ bağlantısı yok"):
        await client.eczaneler.get_list()
