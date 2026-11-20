# Geliştirme Yol Haritası (Roadmap)

Bu belge, `izmir-open-data-py` projesinin tamamlanan ve planlanan teknik kilometre taşlarını listeler.

## v0.1.0: Temel İstemci ve Uç Noktalar (Tamamlandı)

- [x] `httpx` tabanlı asenkron çekirdek istemci motoru.
- [x] Pydantic V2 modelleri ile tip güvenliği ve otomatik veri doğrulama.
- [x] 30 belediye REST ve CBS uç noktası (ESHOT, İZBAN, Metro, İZSU, BİSİM, Eczaneler vb.).
- [x] FastMCP stdio sunucusu (`izmir-mcp`).
- [x] Temel `izmir-data get` CLI komutu.

## v0.2.0: CKAN, Güvenlik, Dayanıklılık ve Veri İşleme (Tamamlandı)

- [x] **Açık Veri CKAN Entegrasyonu:** `search_packages`, `get_package`, `list_packages`, `search_datastore`, `dump_datastore`.
- [x] **CKAN Query Builder:** Zincirleme filtreleme, sıralama, arama ve otomatik sayfalama (`fetch_all`).
- [x] **In-Memory TTL Önbellek:** Yapılandırılabilir `MemoryCache` ve FIFO tahliye desteği.
- [x] **Yeniden Deneme Katmanı (Retry):** Rastgele sapmalı (jitter) üstel geri çekilme middleware.
- [x] **GeoJSON Geometri Dönüştürücüsü:** Belediye koordinat formatlarını RFC 7946 GeoJSON FeatureCollection nesnelerine çeviren yardımcılar.
- [x] **Yeni Belediye Servisleri:** Akıllı tuvaletler (`tuvalet`), İtfaiye (`itfaiye`), Ulaşım Merkezi (`izum`), Turuncu Çember (`turuncucember`).
- [x] **Gelişmiş CLI:** `izmir-data search` ve `izmir-data datastore` komutları.
- [x] **Güvenlik Sertleştirmesi:** Path traversal ve SSRF koruması, CSV prototip/alan enjeksiyonu koruması, URL-encoding.

## v0.3.0: Veri Bilimi Entegrasyonları ve Gelişmiş İstemci (Planlanan)

- [ ] Polars ve Pandas DataFrame doğrudan dışa aktarım desteği (`to_dataframe()`, `to_polars()`).
- [ ] Toplu API çağrıları için asenkron jeneratör akışları (async generator stream).
- [ ] Çevrimdışı testler için dahili sahte veri seti üreticisi (offline test fixtures).
- [ ] Parquet ve GeoParquet formatında yerel depolama araçları.
