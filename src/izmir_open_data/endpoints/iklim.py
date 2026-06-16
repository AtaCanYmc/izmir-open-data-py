from datetime import date

from pydantic import BaseModel, Field

from izmir_open_data.endpoints.base import BaseEndpoint


class HavaKalitesiOlcum(BaseModel):
    olcum_tarihi: str = Field(alias="OlcumTarihi")
    bolge_id: int = Field(alias="BolgeId")
    bolge_adi: str = Field(alias="BolgeAdi")
    gaz_id: int = Field(alias="GazId")
    gaz_adi: str = Field(alias="GazAdi")
    olcum_degeri: str = Field(alias="OlcumDegeri")


class HavaKalitesiIstasyonu(BaseModel):
    """
    Hava kalitesi ölçüm istasyonu bilgisi (CSV datasından)
    """

    bolge: int | str = Field(alias="BOLGE", description="Bölge ID'si")
    ilce: str = Field(alias="ILCE", description="İlçe adı")
    istasyon_adi: str = Field(alias="ISTASYON_ADI", description="İstasyon adı")
    enlem: float | str = Field(alias="ENLEM", description="Enlem (latitude)")
    boylam: float | str = Field(alias="BOYLAM", description="Boylam (longitude)")


class IklimEndpoint(BaseEndpoint):
    async def get_gunluk_hava_kalitesi_olcumleri(
        self, tarih: date
    ) -> list[HavaKalitesiOlcum]:
        """
        Belirtilen tarihe göre hava kalitesi ölçüm değerlerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/hava-kalitesi-olcum-degerleri
        """
        tarih_str = tarih.strftime("%Y-%m-%d")
        return await self._client.get(f"ibb/cevre/havadegerleri/{tarih_str}")

    async def get_hava_kalitesi_istasyonlari(self) -> list[HavaKalitesiIstasyonu]:
        """
        Hava kalitesi ölçüm istasyonlarının konum bilgilerini içeren web servisi (CSV).

        Kaynak: https://acikveri.bizizmir.com/dataset/hava-kalitesi-olcum-istasyonlari
        """
        return await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/3712094a-ded4-40cf-ac94-2102eeb73cbc/resource/7b0edbda-350a-4240-b2c5-a4deb1b4bdfc/download/hava-kalitesi-olcum-istasyonlari.csv"
        )
