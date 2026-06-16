# Izmir Open Data Python Client 🏙️

Izmir Büyükşehir Belediyesi Açık Veri Portalı için resmi olmayan Python kütüphanesi ve MCP (Model Context Protocol) sunucusu.

Bu kütüphane `izmir-open-data-js` projesinin Python karşılığıdır.

## Özellikler
- 🚀 Modern, `async` tabanlı API istemcisi (`httpx`)
- 💻 Kullanışlı Komut Satırı Arayüzü (CLI) (`typer`)
- 🤖 Model Context Protocol (MCP) Desteği (`fastmcp`)
- 🛡️ Tam statik tip desteği ve Pydantic modelleri

## Hızlı Başlangıç (Quick Start)

Geliştirme ortamını kurmak için aşağıdaki adımları izleyin. Bu projede modern ve hızlı olduğu için `uv` kullanılması önerilir (alternatif olarak standart `pip` veya `poetry` de kullanabilirsiniz).

```bash
# 1. Proje dizininde Git'i başlatın
git init

# 2. Python sanal ortamını (virtual environment) oluşturun ve aktifleştirin
# uv kullanıyorsanız:
uv venv
source .venv/bin/activate

# 3. Bağımlılıkları geliştirici araçlarıyla birlikte yükleyin
uv pip install -e ".[dev]"
# veya standart pip ile: pip install -e ".[dev]"

# 4. Pre-commit hook'larını kurun
# Bu adım, her commit öncesi kodun otomatik olarak lint (ruff) ve type-check (mypy) işleminden geçmesini sağlar.
pre-commit install
```

## Kullanım

### CLI Olarak
```bash
izmir-data get hal-fiyatlari
```

### Kütüphane Olarak
```python
import asyncio
from src.izmir_open_data.core.client import IzmirClient

async def main():
    async with IzmirClient() as client:
        data = await client.get_dataset("hal-fiyatlari")
        print(data)

asyncio.run(main())
```

### MCP Sunucusu Olarak
```bash
izmir-mcp
```

## Lisans

Bu proje [Apache License 2.0](LICENSE) altında lisanslanmıştır.
