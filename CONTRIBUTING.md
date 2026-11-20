# Katkıda Bulunma Rehberi (Contributing Guide)

`izmir-open-data-py` projesine katkıda bulunmak istediğiniz için teşekkürler. Bu kılavuz, geliştirme sürecini tutarlı ve yüksek standartta tutmak için hazırlanmıştır.

## Geliştirme Ortamı Kurulumu

Projeyi yerel ortamınızda çalıştırmak için Python 3.11 veya üzeri ve `uv` paket yöneticisi önerilir:

```bash
# Repoyu klonlayın
git clone https://github.com/AtaCanYmc/izmir-open-data-py.git
cd izmir-open-data-py

# Geliştirme bağımlılıklarıyla sanal ortamı kurun
uv pip install -e ".[dev]"
```

## Dal (Branch) İsimlendirme Kuralları

Yeni bir özellik veya hata düzeltmesi üzerinde çalışırken dal isimlendirmesinde şu standartları izleyin:

- Özellik eklemeleri: `feat/ozellik-adi`
- Hata düzeltmeleri: `fix/hata-tanimi`
- Dokümantasyon: `docs/dosya-adi`
- Yeniden yapılandırma: `refactor/bilesen-adi`

## Commit Mesajı Formatı (Conventional Commits)

Commit mesajları `Conventional Commits` formatına uygun olmalıdır:

- `feat: ckan sorgu olusturucu destegi eklendi`
- `fix: path traversal acigi kapatildi`
- `docs: CLI kilavuzu guncellendi`
- `test: onbellek tahliye birim testleri eklendi`
- `refactor: retry fonksiyonu sadelestirildi`

## Doğrulama ve Test Adımları

Pull Request açmadan önce tüm yerel kontrollerin başarılı olduğundan emin olun:

```bash
# 1. Birim testlerini calistirin
uv run pytest

# 2. Kod standartlari ve lint kontrolu
uv run ruff check .

# 3. Kod bicimlendirme kontrolu
uv run ruff format --check .

# 4. Statik tip denetimi
uv run mypy src
```

## Pull Request Süreci

1. Yeni özellikler için ilgili birim testlerini ekleyin.
2. Gerekli durumlarda `docs/` ve `README.md` dokümanlarını güncelleyin.
3. PR açıklamasında yapılan değişiklikleri ve doğrulama çıktılarını maddeler halinde belirtin.
