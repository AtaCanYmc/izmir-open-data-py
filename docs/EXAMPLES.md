# Kod Örnekleri Kılavuzu (Examples Guide)

Bu rehber, `examples/` dizini altında bulunan çalıştırılabilir Python betiklerinin işlevlerini ve çalıştırma komutlarını açıklar.

## Örnek Dosyalar Listesi

| Dosya | Açıklama | Çalıştırma |
| --- | --- | --- |
| `examples/ckan_example.py` | CKAN portalı arama, akıllı tuvaletler, itfaiye ve İZUM seyahat süreleri sorguları. | `python examples/ckan_example.py` |
| `examples/scraper_example.py` | HTML içerik çözümleme ve web kazıma entegrasyonu. | `python examples/scraper_example.py` |
| `examples/mcp_example.py` | FastMCP istemci bağlantısı ve tool çalıştırma örneği. | `python examples/mcp_example.py` |
| `examples/cli_example.sh` | Terminal CLI arayüzünün bash üzerinden toplu test senaryoları. | `bash examples/cli_example.sh` |

---

## Örnekleri Çalıştırma

Tüm örnekleri çalıştırmadan önce bağımlılıkları yükleyin:

```bash
uv pip install -e ".[dev]"
```

### 1. CKAN ve Yeni Modüller Örneği

```bash
python examples/ckan_example.py
```

Bu betik sırasıyla şu adımları icra eder:
1. `client.ckan.search_packages("tuvalet", rows=3)` çağrısıyla portalda arama yapar.
2. `client.tuvalet.get_akilli_tuvaletler(filters={"ILCE": "KONAK"})` ile Konak ilçesindeki tuvaletleri listeler.
3. `client.itfaiye.get_gruplar()` ile itfaiye istasyonlarını çeker.
4. `client.izum.get_ana_arter_hiz_ve_sure(limit=2)` ile ana arter hız ve süre verilerini ekrana basar.

### 2. CLI Komut Örnekleri (Bash)

```bash
bash examples/cli_example.sh
```

Terminal üzerinde Rich formatında tablo çıktılarını doğrulamak için kullanılır.
