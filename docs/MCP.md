# İzmir Open Data MCP Sunucusu Dokümantasyonu

Projemiz, yapay zeka asistanlarının (Örn: Claude Desktop, ChatGPT, vb.) İzmir Büyükşehir Belediyesi Açık Veri Portalı ile doğrudan etkileşim kurabilmesi için **Model Context Protocol (MCP)** standartlarını tam olarak destekler.

`izmir-open-data-py`, `FastMCP` altyapısı üzerine inşa edilmiş entegre bir sunucu sunmaktadır.

## Nasıl Başlatılır?

Kurulum yaptıktan sonra, terminalinizden MCP sunucusunu başlatmak oldukça basittir:

```bash
# Geliştirici / Debug modunda başlatmak için:
izmir-mcp dev

# Standart MCP I/O aktarımı ile (örneğin Claude Desktop için) başlatmak için:
izmir-mcp run
```

Bu komut, yerel bilgisayarınızda bir MCP Server ayağa kaldırır ve LLM ajanlarının bağlanıp veriyi kullanmasını sağlar.

## Claude Desktop ile Kurulum

`Claude Desktop` uygulamasını İzmir verileriyle entegre etmek için konfigürasyon dosyanıza (`claude_desktop_config.json`) şu tanımlamayı ekleyebilirsiniz:

```json
{
  "mcpServers": {
    "izmir-open-data": {
      "command": "izmir-mcp",
      "args": ["run"]
    }
  }
}
```

*Not: Eğer paketi bir sanal ortam (`.venv`) içine kurduysanız, `command` kısmına sanal ortamınızın içindeki `izmir-mcp` (örn: `/path/to/project/.venv/bin/izmir-mcp`) mutlak yolunu yazmanız gerekmektedir.*

## LLM (Yapay Zeka) İçin Sağlanan Araçlar (Tools)

Sunucuya bağlanan LLM'ler İzmir verilerini tamamen bağımsız olarak keşfedip sorgulayabilir. Sunucu şu araçları dışarıya (expose) sunar:

### 1. `list_endpoints()`
Sunucuya bağlanan asistanın **"Hangi verilere erişebilirim?"** sorusunun cevabıdır. `IzmirClient` içerisindeki tüm namespace'leri (örn. `eshot`, `bisim`) ve bu gruplar içindeki metotları (örn. `get_istasyon_list`) dinamik olarak tarar.

**Örnek Çıktı:**
```json
[
  "bisim.get_istasyon_list: BİSİM istasyonlarının kapasite bilgilerini içeren web servisi.",
  "otopark.get_list: Otoparkların konumu ve doluluk oranlarını içerir.",
  "kamu.get_hastaneler_list: İzmir'deki hastaneleri listeler."
]
```

### 2. `call_endpoint(namespace, endpoint_name, kwargs_dict)`
LLM, `list_endpoints` aracı ile ulaştığı herhangi bir servisi doğrudan bu komutla çalıştırabilir.

**Örnek LLM Kullanımı:**
```json
{
  "namespace": "bisim",
  "endpoint_name": "get_istasyon_list"
}
```
Asistan, bu tool'u çağırdığında arka planda `await client.bisim.get_istasyon_list()` komutu çalıştırılır ve Pydantic modelleri ile parse edilmiş temiz JSON verisi doğrudan asistana döndürülür.

### 3. `get_dataset(dataset_id)`
*(Not: Geriye dönük uyumluluk ve hızlı cbs/ testleri için barındırılmaktadır. LLM'lerin `call_endpoint` kullanması daha çok tavsiye edilir.)*
Basitçe `ibb/{dataset_id}` yoluna raw HTTP Get isteği atar ve json sonucunu döner.

---

Yapay Zeka ajanı yukarıdaki araçlar vasıtasıyla sizin hiçbir müdahalenize gerek kalmadan şuna benzer komutları anlar ve gerçek verilerle cevaplar:

> **İnsan:** "Şu an Karşıyaka'daki hangi BİSİM istasyonlarında boş bisiklet var?"
>
> **AI:** *(Arka planda `list_endpoints` ile bisim servisini bulur, `call_endpoint` ile veriyi çeker ve JSON sonucunu yorumlayarak size sözel cevap verir.)* "Karşıyaka İskele istasyonunda şu an 12 boş bisiklet bulunuyor..."
