"""
Scraper (API Client) Kullanım Örneği

Bu örnek, IzmirClient kullanarak İzmir Açık Veri Portalı'ndan asenkron olarak 
nasıl veri çekileceğini gösterir.
"""
import asyncio
from izmir_open_data.core.client import IzmirClient


async def main():
    # İstemciyi başlatın (Bazı verisetleri API anahtarı gerektirmeyebilir)
    # Async context manager (async with) kullanımı bağlantıların düzgün kapanmasını sağlar.
    async with IzmirClient() as client:
        print("'afet_toplanma_alanlari' veriseti çekiliyor...")
        data = await client.afetler.get_acil_durum_toplanma_alanlari()
        
        print("\nVeri başarıyla çekildi!")
        
        if "kayitlar" in data:
            print(f"Toplam kayıt sayısı: {data.get('kayit_sayisi')}")
            print("İlk 2 kayıt:")
            print(data["kayitlar"][:2])
        else:
            print("Ham Yanıt Özeti:")
            print(str(data)[:500] + "...\n(devamı var)")


if __name__ == "__main__":
    # Asenkron main fonksiyonunu çalıştır
    asyncio.run(main())
