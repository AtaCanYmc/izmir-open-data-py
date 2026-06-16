"""
Scraper (API Client) Kullanım Örneği

Bu örnek, IzmirClient kullanarak İzmir Açık Veri Portalı'ndan asenkron olarak 
nasıl veri çekileceğini gösterir.
"""
import asyncio
import json
from src.izmir_open_data.core.client import IzmirClient


async def main():
    # İstemciyi başlatın (Bazı verisetleri API anahtarı gerektirmeyebilir)
    # Async context manager (async with) kullanımı bağlantıların düzgün kapanmasını sağlar.
    async with IzmirClient() as client:
        print("'hal-fiyatlari' veriseti çekiliyor...")
        try:
            # 'hal-fiyatlari' yerine İzmir Açık Veri portalındaki geçerli bir veriseti ID'si yazabilirsiniz.
            data = await client.get_dataset("hal-fiyatlari")

            print("\nVeri başarıyla çekildi!")

            # Örnek olarak ilk 2 kaydı yazdıralım
            # Not: Yanıt yapısı endpoint'e göre değişiklik gösterebilir
            if "kayitlar" in data:
                print(f"Toplam kayıt sayısı: {data.get('kayit_sayisi', len(data['kayitlar']))}")
                print("İlk 2 kayıt:")
                print(json.dumps(data["kayitlar"][:2], indent=2, ensure_ascii=False))
            else:
                print("Ham Yanıt Özeti:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...\n(devamı var)")

        except Exception as e:
            print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    # Asenkron main fonksiyonunu çalıştır
    asyncio.run(main())
