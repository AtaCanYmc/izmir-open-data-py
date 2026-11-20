# İzmir Open Data Client (İstemci) Dokümantasyonu

`IzmirClient` (veya takma adıyla `IzmirAPI`), İzmir Büyükşehir Belediyesi Açık Veri Portalı ve Open API servislerine bağlanmanızı sağlayan asenkron, tip güvenli bir Python istemcisidir. `httpx` ve `pydantic` tabanlı geliştirilmiş olup REST, CSV ve CKAN Datastore servisleri için birleşik bir arayüz sunar.

## Temel Kullanım

İstemciyi asenkron bir context manager içinde kullanmak, bağlantı havuzlarının güvenle yönetilmesini sağlar:

```python
import asyncio
from izmir_open_data import IzmirClient


async def main():
    async with IzmirClient() as client:
        # Nöbetçi eczaneler
        nobetci = await client.eczaneler.get_nobetci_list()
        print(f"Nöbetçi eczane sayısı: {len(nobetci)}")

        # BİSİM istasyon durumları
        istasyonlar = await client.bisim.get_istasyon_list()
        for ist in istasyonlar.kayitlar[:3]:
            print(f"{ist.adi}: {ist.bos_bisiklet_sayisi} bisiklet")


asyncio.run(main())
```

Context manager dışında kullanıldığında işiniz bittiğinde `await client.close()` çağrılmalıdır.

## Gelişmiş Özellikler

### 1. In-Memory TTL Önbellek (Cache)

Belediye sunucularına gereksiz tekrarlı istekleri önlemek için dahili bellek önbelleği:

```python
from izmir_open_data import IzmirClient, MemoryCache

# 5 dakika varsayılan TTL ile önbelleği aktifleştirme
client = IzmirClient(cache=True)

# Özel TTL (milisaniye) ve azami kayıt adedi ile:
custom_client = IzmirClient(cache=MemoryCache(default_ttl_ms=60_000, max_items=200))

# İlk istek ağdan çekilir, ikincisi önbellekten anında döner
data1 = await client.eczaneler.get_nobetci_list()
data2 = await client.eczaneler.get_nobetci_list()

# Önbelleği temizleme
await client.clear_cache()
```

### 2. İstek Yeniden Deneme (Retry Middleware with Jitter)

Geçici sunucu (5xx, 429) ve ağ hatalarında üstel geri çekilme ve rastgele sapma (jitter):

```python
from izmir_open_data import IzmirClient, RetryConfig

client = IzmirClient(
    retry=RetryConfig(
        retries=3,  # Azami 3 deneme
        base_delay_ms=300,  # Başlangıç beklemesi
        max_delay_ms=3000,  # Tavan bekleme
        jitter=True,  # Yük yığılmasını önleyen sapma
    )
)
```

### 3. CKAN Akıcı Sorgu Oluşturucu (Query Builder)

CKAN Datastore kaynakları üzerinde zincirleme filtreleme, metin araması, sıralama ve sayfalama:

```python
query = (
    client.ckan.query("d87de3c1-9bc0-4a8c-842a-90cd2a30d03a")
    .where("ILCE", "KONAK")
    .search("Alsancak")
    .sort("TARIH", "desc")
    .page(1, 20)
)

# İlk sayfayı çekme
result = await query.execute()
print(result["records"])

# Otomatik sayfalama ile tüm kayıtları çekme
all_records = await query.fetch_all(batch_size=100, max_records=500)
```

### 4. GeoJSON Geometri Dönüştürücüsü

Belediyenin farklı koordinat formatlarını (CBS `BOYLAM`/`ENLEM`, Yazılım Şube `LokasyonX`/`LokasyonY`) standart RFC 7946 GeoJSON formatına dönüştürür:

```python
from izmir_open_data import to_geojson, extract_coordinates

# Tekil nokta koordinatını (boylam, enlem) olarak ayıklama
coords = extract_coordinates({"LokasyonX": "38.4192", "LokasyonY": "27.1287"})
# (27.1287, 38.4192)

# Belediye mekan verilerini FeatureCollection formatına dönüştürme
parklar = await client.cografi.get_meydanlar_list()
geojson_data = to_geojson(parklar)

print(geojson_data["type"])  # "FeatureCollection"
print(geojson_data["features"][0]["geometry"]["coordinates"])
```

### 5. Pandas & Polars DataFrame Dışa Aktarımı

Veri analitiği ve yapay zeka iş akışları için tek satırda DataFrame dönüşümü:

```python
from izmir_open_data import to_dataframe, to_polars

# Herhangi bir API yanıtını Pandas veya Polars tablosuna çevirme
eczane_listesi = await client.eczaneler.get_list()
df = to_dataframe(eczane_listesi)
pldf = to_polars(eczane_listesi)

# CKAN Query Builder üzerinden doğrudan:
df = await client.ckan.query("res-uuid").where("ILCE", "KONAK").to_dataframe()
pldf = await client.ckan.query("res-uuid").where("ILCE", "KONAK").to_polars()
```

### 6. Asenkron Jeneratör Akışları (Streams)

Büyük veri setlerini (10.000+ kayıt) belleği şişirmeden akış halinde işleme:

```python
# Kayıt bazlı akış (item by item)
async for record in client.ckan.query("res-uuid").stream(batch_size=200):
    print(record["_id"], record.get("TESIS_ADI"))

# Paket bazlı akış (batch by batch)
async for batch in client.ckan.query("res-uuid").stream_batches(batch_size=500):
    print(f"Alınan paket boyutu: {len(batch)}")
```

### 7. Parquet ve GeoParquet Depolama Araçları

Verileri sıkıştırılmış sütun tabanlı Parquet veya WKB geometrili GeoParquet v1.1.0 formatında saklama:

```python
from izmir_open_data import to_parquet, read_parquet, to_geoparquet

# Parquet olarak kaydetme ve okuma
await client.ckan.query("res-uuid").to_parquet("veriler.parquet")
records = read_parquet("veriler.parquet")

# CBS verilerini standart GeoParquet olarak dışa aktarma (QGIS / DuckDB uyumlu)
parklar = await client.cografi.get_meydanlar_list()
to_geoparquet(parklar, "meydanlar.geoparquet")
```

### 8. Çevrimdışı Test Altyapısı (Mock Client)

Ağ erişimi gerektirmeden birim testleri koşturmak veya air-gapped ortamlarda çalışmak için:

```python
from izmir_open_data import MockIzmirClient, get_fixture

# Hazır fikstür verisine erişim
eczaneler = get_fixture("eczaneler")

# Mock istemci ile ağ isteği atmadan geliştirme yapma
client = MockIzmirClient()
nobetci = await client.eczaneler.get_list()
assert len(nobetci) > 0
```

## Endpoint Grupları (Namespaces)

- **Ulaşım:** `client.eshot`, `client.izban`, `client.metro`, `client.tramvay`, `client.vapur`, `client.taksi`, `client.izum`
- **Gündelik Yaşam:** `client.bisim`, `client.otopark`, `client.trafik`, `client.izmirimkart`, `client.wizmirnet`
- **Kent, Sağlık & Hijyen:** `client.eczaneler`, `client.saglik`, `client.afetler`, `client.iklim`, `client.izsu`, `client.tuvalet`, `client.turuncucember`, `client.itfaiye`
- **Sosyal & Kültürel:** `client.etkinlikler`, `client.kutuphane`, `client.spor`, `client.tarihi`, `client.plaj`, `client.sosyal`
- **Şehir Rehberi & Kamu:** `client.kamu`, `client.hizmet`, `client.pazarlar`, `client.egitim`, `client.muhtarliklar`, `client.cografi`, `client.iztek`, `client.tren`
- **CKAN Açık Veri Portalı:** `client.ckan`
