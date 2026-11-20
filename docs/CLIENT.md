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

## Endpoint Grupları (Namespaces)

- **Ulaşım:** `client.eshot`, `client.izban`, `client.metro`, `client.tramvay`, `client.vapur`, `client.taksi`, `client.izum`
- **Gündelik Yaşam:** `client.bisim`, `client.otopark`, `client.trafik`, `client.izmirimkart`, `client.wizmirnet`
- **Kent, Sağlık & Hijyen:** `client.eczaneler`, `client.saglik`, `client.afetler`, `client.iklim`, `client.izsu`, `client.tuvalet`, `client.turuncucember`, `client.itfaiye`
- **Sosyal & Kültürel:** `client.etkinlikler`, `client.kutuphane`, `client.spor`, `client.tarihi`, `client.plaj`, `client.sosyal`
- **Şehir Rehberi & Kamu:** `client.kamu`, `client.hizmet`, `client.pazarlar`, `client.egitim`, `client.muhtarliklar`, `client.cografi`, `client.iztek`, `client.tren`
- **CKAN Açık Veri Portalı:** `client.ckan`
