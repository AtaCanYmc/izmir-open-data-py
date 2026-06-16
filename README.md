<p align="center">
  <img src="assets/logo.png" width="300" alt="Izmir Open Data Logo">
</p>

<h1 align="center">İzmir Open Data · Python İstemcisi</h1>

<p align="center">
  <i>İzmir Büyükşehir Belediyesi Açık Veri Portalı ve Open API servisleri için modern, asenkron ve tip güvenli (Pydantic) Python istemcisi.</i>
</p>

<p align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python 3.10+">
  </a>
  <a href="https://pydantic.dev">
    <img src="https://img.shields.io/badge/Pydantic-v2-e92063.svg?logo=pydantic&logoColor=white" alt="Pydantic v2">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://mypy.readthedocs.io/en/stable/">
    <img src="https://img.shields.io/badge/mypy-checked-1f5082.svg" alt="Mypy checked">
  </a>
  <a href="https://modelcontextprotocol.io/">
    <img src="https://img.shields.io/badge/MCP-Ready-success.svg?logo=server&logoColor=white" alt="MCP Ready">
  </a>
</p>

---

## 🚀 Özellikler

- **Tam Asenkron Destek:** `httpx` altyapısı ile non-blocking, yüksek performanslı istekler.
- **%100 Tip Güvenliği:** API yanıtları Pydantic V2 modellerine dönüştürülür, IDE'lerde otomatik tamamlama (autocompletion) desteği sunar.
- **Kapsamlı Kapsama Alanı:** ESHOT, İZBAN, Metro, Vapur, BİSİM, İZSU, Otopark, Etkinlikler, Hal Fiyatları ve daha birçok servisi kapsayan ~150 endpoint desteği. *(Bütün metodların listesini [Tüm Endpointler Listesi (docs/ENDPOINTS.md)](docs/ENDPOINTS.md) dosyasından inceleyebilirsiniz.)*
- **CLI (Komut Satırı) Aracı:** Terminal üzerinden doğrudan açık veriye erişebilme imkanı.
- **Model Context Protocol (MCP):** AI ajanlarının (Claude, vb.) doğrudan açık veriyi sorgulayabilmesi için hazır bir MCP sunucusu.

## 📦 Kurulum

Şu anda paket kaynak koddan yüklenebilmektedir (ileride PyPI'a eklenebilir):

```bash
# Repoyu klonlayın
git clone https://github.com/AtaCanYmc/izmir-open-data-py.git
cd izmir-open-data-py

# pip ile (tercihen sanal ortamda) kurun
pip install -e .
```

## 📖 Temel Kullanım

```python
import asyncio
from izmir_open_data import IzmirClient

async def main():
    async with IzmirClient() as client:
        # BİSİM İstasyonları ve Boş Bisiklet Durumları
        istasyonlar = await client.bisim.get_istasyon_list()
        for ist = istasyonlar.kayitlar[:3]:
            print(f"İstasyon: {ist.adi} | Boş Bisiklet: {ist.bos_bisiklet_sayisi}")

        # Otopark Doluluk Oranları
        otoparklar = await client.otopark.get_list()
        for oto in otoparklar[:3]:
            print(f"Otopark: {oto.name} | Boş Yer: {oto.occupancy.total.free}")

if __name__ == "__main__":
    asyncio.run(main())
```

> Daha detaylı istemci mimarisi ve namespace yapıları için [İstemci (Client) Dokümantasyonuna (docs/CLIENT.md)](docs/CLIENT.md) göz atın.

## 💻 CLI (Komut Satırı) Aracı

Terminal üzerinden herhangi bir script yazmadan İzmir verilerine ulaşabilirsiniz.

```bash
# Yardım menüsü
izmir-data --help

# İstediğiniz veri setini çekmek (örn: afet toplanma alanları)
izmir-data get cbs/afetaciltoplanmaalani
```

## 🤖 MCP (Model Context Protocol) Sunucusu

Proje entegre bir MCP sunucusuyla gelmektedir. Yapay zeka ajanlarına izmir verilerini öğretmek isterseniz:

```bash
# FastMCP sunucusunu başlatın
izmir-mcp dev
```

Yapay zeka asistanları (Örn. Claude), bu sunucuya bağlandıklarında sistemdeki tüm API'leri kendi başlarına tarayabilir ve sorularınızı gerçek zamanlı verilerle cevaplayabilir.

> MCP sunucusunun yetenekleri, LLM araçları ve Claude Desktop entegrasyonu için detaylı [MCP Dokümantasyonuna (docs/MCP.md)](docs/MCP.md) göz atın.

## 🧪 Testler ve Geliştirme

Proje kod kalitesini sağlamak için `ruff`, `mypy` ve `pre-commit` kullanmaktadır. Canlı endpoint testleri `pytest` ile yazılmıştır:

```bash
# Canlı veritabanına bağlanıp 150 endpointin anlık durumunu test edin
pytest tests/
```

## 📄 Lisans

Bu proje **Apache License 2.0** altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.
