import asyncio

from izmir_open_data import IzmirClient


async def main() -> None:
    print("=== İzmir Açık Veri Portalı: CKAN ve Yeni Modüller ===\n")
    async with IzmirClient() as client:
        # 1. CKAN Veri Seti Arama
        print("1. CKAN Portalı Üzerinde 'tuvalet' Araması Yapılıyor...")
        search_result = await client.ckan.search_packages("tuvalet", rows=3)
        print(f"Bulunan Veri Seti Sayısı: {search_result.get('count', 0)}")
        for pkg in search_result.get("results", []):
            print(
                f"  - {pkg.get('title')} ({pkg.get('name')}) [{pkg.get('num_resources')} kaynak]"
            )

        # 2. Akıllı Tuvaletler
        print("\n2. Akıllı Tuvaletler Sorgulanıyor (Konak İlçesi)...")
        tuvaletler = await client.tuvalet.get_akilli_tuvaletler(
            filters={"ILCE": "KONAK"}, limit=2
        )
        print(f"Konak'taki Akıllı Tuvalet Sayısı: {tuvaletler.get('total', 0)}")
        for wc in tuvaletler.get("records", []):
            print(
                f"  - {wc.get('TESIS_ADI')} ({wc.get('ADRES')}) [{wc.get('ENLEM')}, {wc.get('BOYLAM')}]"
            )

        # 3. İtfaiye Grupları (CBS)
        print("\n3. İtfaiye İstasyonları ve Grupları Listeleniyor...")
        itfaiye_gruplari = await client.itfaiye.get_gruplar()
        ilk_iki = (
            itfaiye_gruplari.get("onemliyer", [])
            if isinstance(itfaiye_gruplari, dict)
            else []
        )[:2]
        for g in ilk_iki:
            print(f"  - {g.get('ADI')} ({g.get('ILCE')})")

        # 4. İZUM Ana Arter Hız ve Seyahat Süresi Verileri
        print("\n4. İZUM Ana Arterler Hız ve Seyahat Süreleri Sorgulanıyor...")
        hizlar = await client.izum.get_ana_arter_hiz_ve_sure(limit=2)
        for h in hizlar.get("records", []):
            print(
                f"  - {h.get('BASLAMA')} -> {h.get('BITIS')} | Hız: {h.get('HIZ')} km/s, Süre: {h.get('SURE')} dk ({h.get('SAAT')})"
            )

        print("\nİşlem başarıyla tamamlandı.")


if __name__ == "__main__":
    asyncio.run(main())
