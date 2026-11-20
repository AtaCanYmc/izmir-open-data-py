# İzmir Open Data Terminal CLI Dokümantasyonu

`izmir-data`, İzmir Büyükşehir Belediyesi Açık Veri Portalı ve REST servislerini terminal üzerinden doğrudan sorgulamak için geliştirilmiş bir komut satırı aracıdır.

## Kurulum ve Çalıştırma

Projeyi yerel olarak kurduğunuzda `izmir-data` komutu terminalinizde kullanılabilir hale gelir:

```bash
uv pip install -e .
```

Komut çalıştırıldığında yardım ve seçenekler:

```bash
izmir-data --help
```

---

## Komutlar

### 1. `izmir-data get <dataset_id>`

Belirli bir belediye CBS veya REST veri setini çeker ve terminalde yapılandırılmış bir Rich tablosunda görüntüler.

**Kullanım:**
```bash
izmir-data get <dataset_id>
```

**Örnekler:**
```bash
# Afet ve acil durum toplanma alanları
izmir-data get cbs/afetaciltoplanmaalani

# İzmir genelindeki plajlar
izmir-data get cbs/plajlar

# Hastaneler ve sağlık merkezleri
izmir-data get cbs/hastaneler

# BİSİM akıllı bisiklet istasyonları
izmir-data get cbs/bisimistasyon
```

*Not: Terminal okunabilirliğini korumak için ilk 6 sütun gösterilir. Ek sütunlar tablo altında bilgi kutusu olarak listelenir.*

---

### 2. `izmir-data search <query>`

`acikveri.bizizmir.com` portalındaki 260'tan fazla veri setinde başlık, etiket ve açıklama araması yapar.

**Kullanım:**
```bash
izmir-data search <query> [--limit <sayi>]
```

**Parametreler:**
- `<query>`: Arama terimi (Örn: `tuvalet`, `otopark`, `itfaiye`, `eshot`)
- `-l, --limit`: Dönecek azami sonuç sayısı (Varsayılan: `10`)

**Örnekler:**
```bash
# Tuvalet ile ilgili veri setlerini listeleme
izmir-data search tuvalet --limit 5

# Otopark verilerini listeleme
izmir-data search otopark
```

**Örnek Çıktı:**
```text
Toplam bulunan veri seti: 2 (Gösterilen: 2)

┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ ID / Slug           ┃ Başlık                                      ┃ Kaynak Sayısı ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ akilli-tuvaletler   │ Akıllı Tuvaletler                           │ 2             │
│ moduler-tuvaletler  │ Modüler Sistem Tuvalet ve Bebek Bakım Alanı │ 2             │
└─────────────────────┴─────────────────────────────────────────────┴───────────────┘
```

---

### 3. `izmir-data datastore <resource_id>`

Belirli bir CKAN Datastore kaynağının (resource UUID) kayıtlarını filtreler ve tablo halinde listeler.

**Kullanım:**
```bash
izmir-data datastore <resource_id> [--limit <sayi>] [--query <metin>]
```

**Parametreler:**
- `<resource_id>`: CKAN Resource UUID (Örn: `d87de3c1-9bc0-4a8c-842a-90cd2a30d03a`)
- `-l, --limit`: Çekilecek kayıt adedi (Varsayılan: `10`)
- `-q, --query`: Tam metin arama filtresi

**Örnekler:**
```bash
# Akıllı tuvaletler kaynağından ilk 5 kaydı çekme
izmir-data datastore d87de3c1-9bc0-4a8c-842a-90cd2a30d03a --limit 5

# Alsancak bölgesindeki kayıtları arama
izmir-data datastore d87de3c1-9bc0-4a8c-842a-90cd2a30d03a --query Alsancak
```
