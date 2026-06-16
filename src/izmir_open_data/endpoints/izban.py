from typing import Any

from pydantic import BaseModel, Field

from izmir_open_data.endpoints.base import BaseEndpoint


class IzbanUcretDetay(BaseModel):
    binis_istasyonu: str = Field(alias="BinisIstasyonu")
    inis_istasyonu: str = Field(alias="InisIstasyonu")
    toplam_km: float = Field(alias="ToplamKm")
    
    tam_ucret: float = Field(alias="TamUcret")
    ogrenci_ucret: float = Field(alias="OgrenciUcret")
    ogretmen_ucret: float = Field(alias="OgretmenUcret")
    yas60_ucret: float = Field(alias="Yas60Ucret")
    serbest_ucret: float = Field(alias="SerbestUcret")
    
    iade_tam: float = Field(alias="IadeTam")
    iade_ogrenci: float = Field(alias="IadeOgrenci")
    iade_ogretmen: float = Field(alias="IadeOgretmen")
    iade_60yas: float = Field(alias="Iade60Yas")
    iade_serbest: float = Field(alias="IadeSerbest")
    
    min_bakiye_tam: float = Field(alias="MinBakiyeTam")
    min_bakiye_ogrenci: float = Field(alias="MinBakiyeOgrenci")
    min_bakiye_ogretmen: float = Field(alias="MinBakiyeOgretmen")
    min_bakiye_60yas: float = Field(alias="MinBakiye60Yas")
    min_bakiye_serbest: float = Field(alias="MinBakiyeSerbest")

class IzbanDurakMesafesi(BaseModel):
    """
    İZBAN duraklar arası mesafe bilgisi (CSV datasından)
    İstasyonlar arası mesafe bilgilerini içerir
    """
    istasyon_id: int | str = Field(alias="ISTASYON_ID", description="İstasyon ID'si")
    istasyon_adi: str = Field(alias="ISTASYON_ADI", description="İstasyon adı")
    istasyon_sirasi: int | str = Field(alias="ISTAYON_SIRASI", description="Hat üzerindeki istasyon sırası")
    mesafe: float | str = Field(alias="MESAFE", description="Bir önceki istasyona olan mesafe (metre cinsinden)")

class IzbanEndpoint(BaseEndpoint):
    async def get_tarife(self, binis_istasyonu_id: int, inis_istasyonu_id: int, aktarma: int, htt_mi: int) -> IzbanUcretDetay:
        """
        Banliyö fiyat tarifesi bilgisini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izban-banliyo-fiyat-tarifesi-servisi
        
        Args:
            binis_istasyonu_id: Binilecek istasyonun id'si
            inis_istasyonu_id: İnilecek istasyonun id'si
            aktarma: Kaç kez aktarma yapıldı (0, 1 kez, 2 kez, 3 kez)
            htt_mi: Halk taşıt tarifesi saatleri içerisinde mi?
        """
        return await self._client.get(f"izban/tutarhesaplama/{binis_istasyonu_id}/{inis_istasyonu_id}/{aktarma}/{htt_mi}")

    async def get_istasyon_list(self) -> Any:
        """
        Banliyö İstasyonlarının konum bilgileri içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izban-istasyonlari
        """
        return await self._client.get("izban/istasyonlar")

    async def get_hareket_saatleri(self, kalkis_istasyon_id: int, varis_istasyon_id: int) -> Any:
        """
        Banliyö hareket saatlerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izban-banliyo-hareket-saatleri
        
        Args:
            kalkis_istasyon_id: Kalkış istasyonu ID'si
            varis_istasyon_id: Varış istasyonu ID'si
        """
        return await self._client.get(f"sefersaatleri/{kalkis_istasyon_id}/{varis_istasyon_id}")

    async def get_durak_mesafeleri(self) -> list[IzbanDurakMesafesi]:
        """
        İZBAN istasyonları arasındaki mesafe bilgilerini içeren web servisi (CSV).
        Her istasyonun bir önceki istasyona olan mesafesini metre cinsinden içerir.

        Kaynak: https://acikveri.bizizmir.com/dataset/izban-duraklar-arasi-mesafe
        """
        return await self._client.get_csv(
            'https://acikveri.bizizmir.com/dataset/c40b5759-9394-41b0-a479-0e7c53e18072/resource/53ff5f4b-c514-43aa-a4cd-4a12e03976e1/download/izban-duraklar-arasi-mesafe.csv'
        )
