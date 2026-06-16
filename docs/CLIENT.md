# İzmir Open Data Client (İstemci) Dokümantasyonu

`IzmirClient`, İzmir Büyükşehir Belediyesi Açık Veri Portalı ve Open API servislerine bağlanmanızı sağlayan yüksek performanslı, asenkron bir Python istemcisidir. `httpx` ve `pydantic` tabanlı olarak geliştirilmiştir ve tüm veri türleri (JSON, CSV, CKAN) için standartlaştırılmış bir arayüz sunar.

## Temel Kullanım

İstemciyi asenkron bir bağlam (context manager) içerisinde kullanmak, HTTP oturumlarının düzgün şekilde açılıp kapanmasını sağlar.

```python
import asyncio
from izmir_open_data import IzmirClient

async def main():
    async with IzmirClient() as client:
        # Pydantic modelleri aracılığıyla tip güvenli olarak veri çekin
        istasyonlar = await client.bisim.get_istasyon_list()

        for istasyon in istasyonlar.kayitlar:
            print(f"{istasyon.adi} - Boş Bisiklet: {istasyon.bos_bisiklet_sayisi}")

asyncio.run(main())
```

Eğer bağlam dışında kullanmak isterseniz, işiniz bittiğinde `await client.close()` fonksiyonunu çağırmalısınız.

## Endpoint Grupları (Namespaces)

API içerisindeki 150'den fazla endpoint, kolay erişim için mantıksal gruplara (namespaces) ayrılmıştır. İstemci başlatıldığında bu grupların tümü otomatik olarak yüklenir:

- **Ulaşım:** `client.eshot`, `client.izban`, `client.metro`, `client.tramvay`, `client.vapur`, `client.taksi`
- **Gündelik Yaşam:** `client.bisim`, `client.otopark`, `client.trafik`, `client.izmirimkart`, `client.wizmirnet`
- **Sağlık & Çevre:** `client.eczaneler`, `client.saglik`, `client.afetler`, `client.iklim`, `client.izsu`
- **Sosyal & Kültürel:** `client.etkinlikler`, `client.kutuphane`, `client.spor`, `client.tarihi`, `client.plaj`, `client.sosyal`
- **Şehir Rehberi:** `client.kamu`, `client.hizmet`, `client.pazarlar`, `client.egitim`, `client.muhtarliklar`, `client.cografi`, `client.iztek`, `client.tren`

## Veri Modelleri ve Doğrulama (Pydantic)

İstemci tarafından döndürülen veriler doğrudan `Pydantic` modelleriyle sarılmıştır. Bu sayede IDE'niz (VS Code, PyCharm) size tam kod tamamlama (autocompletion) ve tip güvenliği sunar.

Örneğin, `client.kamu.get_belediyeler_list()` çağrısı bir `OnemliYerWrapper[KamuKurumu]` objesi döner. Tüm önemli yer listeleri şu standart yapıyı izler:

```python
class OnemliYerWrapper(BaseModel, Generic[T]):
    kayit_sayisi: int
    sayfa_numarasi: int
    sayfa_basina_kayit_sayisi: int
    toplam_sayfa_sayisi: int
    kayitlar: list[T] # Verilerin bulunduğu asıl liste
```

Eğer API boş bir yanıt (`null`) dönerse, istemci bunu otomatik olarak boş bir listeye (`[]`) çevirir. Eğer servis kapatılmış veya bakımda ise (404/500 gibi hatalar), istemci standart bir `APIError` fırlatır. Bazı kaldırılmış metotlarda çalışma anında `DeprecationWarning` alabilirsiniz.

## Zaman Aşımı (Timeout) ve Yapılandırma

`IzmirClient` varsayılan olarak **30 saniye** zaman aşımı (timeout) süresine sahiptir, çünkü bazı açık veri servislerinin yanıt vermesi uzun sürebilir. İsterseniz istemci başlatırken API Key ve Base URL ayarlarını ezebilirsiniz (Ancak kütüphane bunları otomatik yönettiği için genelde gerekmez).

```python
client = IzmirClient(api_key="opsiyonel_token")
```
