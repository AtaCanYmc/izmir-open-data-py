# Değişiklik Günlüğü (Changelog)

Bu projedeki tüm önemli değişiklikler bu belgede kayıt altına alınır. Format [Keep a Changelog](https://keepachangelog.com/tr/1.0.0/) standardına uygundur.

## [0.3.0] - 2026-11-20

### Eklendi
- Pandas ve Polars DataFrame dışa aktarım desteği (`to_dataframe()`, `to_polars()`).
- CKANQueryBuilder için doğrudan `.to_dataframe()` ve `.to_polars()` metodları.
- Asenkron jeneratör akışları (`stream()`, `stream_batches()`, `stream_records()`) ile bellek tasarruflu büyük veri işleme.
- Parquet ve GeoParquet v1.1.0 depolama araçları (`to_parquet()`, `read_parquet()`, `to_geoparquet()`).
- Çevrimdışı test fikstürleri (`get_fixture()`, `FIXTURES`) ve ağsız test istemcisi (`MockIzmirClient`).
- Google `release-please` yapılandırması ve GitHub Actions yayınlama iş akışı.

## [0.2.0] - 2026-11-20

### Eklendi
- Açık veri CKAN entegrasyonu (`search_packages`, `get_package`, `list_packages`, `search_datastore`, `dump_datastore`).
- Akıcı CKAN sorgu oluşturucusu (`CKANQueryBuilder`) ve otomatik sayfalama (`fetch_all`).
- In-Memory TTL önbellek sağlayıcısı (`MemoryCache`).
- Jitter destekli üstel geri çekilme yeniden deneme middleware (`execute_with_retry`).
- Koordinat ayıklama ve standart RFC 7946 GeoJSON dönüştürücüleri (`extract_coordinates`, `to_geojson_feature`, `to_geojson`).
- 4 yeni belediye ad alanı: `itfaiye`, `izum`, `turuncucember`, `tuvalet`.
- Terminal CLI arayüzüne `search` ve `datastore` komutları.
- Path traversal, SSRF ve CSV başlık enjeksiyonu güvenlik korumaları.
- Kapsamlı birim test paketi ve `respx` mock entegrasyonu.

### Güncellendi
- `README.md`, `docs/CLIENT.md` ve `docs/ENDPOINTS.md` yeni modül ve özelliklerle genişletildi.
- `IzmirAPI = IzmirClient` takma adı eklendi.
- `pyproject.toml` sürümü `0.2.0` olarak güncellendi ve pytest yapılandırması tamamlandı.

## [0.1.0] - 2026-11-20

### Eklendi
- İlk sürüm: `httpx` ve `pydantic` tabanlı asenkron istemci.
- 30 temel belediye servis modülü (ESHOT, İZBAN, Metro, Vapur, BİSİM, İZSU, Otopark vb.).
- FastMCP stdio sunucusu (`izmir-mcp`).
- Temel `izmir-data get` CLI komutu.
