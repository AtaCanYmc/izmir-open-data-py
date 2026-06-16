from datetime import date

from pydantic import BaseModel

from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class PazarYerleri(DefaultOnemliYer):
    pass


class HalFiyat(BaseModel):
    OrtalamaUcret: float
    MalAdi: str
    Birim: str
    AsgariUcret: float
    AzamiUcret: float
    MalId: int
    tarih: str | None
    HalTuru: int
    MalTipId: int
    MalTipAdi: str
    Gorsel: str


class HalFiyatResponse(BaseModel):
    BultenTarihi: str
    HalFiyatListesi: list[HalFiyat]


class PazarlarEndpoint(BaseEndpoint):
    async def get_list(self) -> OnemliYerWrapper[PazarYerleri]:
        """
        Semt pazar yerlerinin listesi, günleri ve konum bilgileri içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/semt-pazar-yerleri
        """
        return await self._client.get(
            "ibb/cbs/pazaryerleri", response_model=OnemliYerWrapper[PazarYerleri]
        )

    async def get_balik_hal_fiyatlari(self, tarih: date) -> HalFiyatResponse:
        """
        Balık hal fiyatlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/balik-hal-fiyatlari
        """
        formatted_date = tarih.strftime("%Y-%m-%d")
        return await self._client.get(
            f"ibb/halfiyatlari/balik/{formatted_date}",
            response_model=HalFiyatResponse,
        )

    async def get_sebze_meyve_hal_fiyatlari(self, tarih: date) -> HalFiyatResponse:
        """
        Sebze ve meyve hal fiyatlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/sebze-ve-meyve-hal-fiyatlari
        """
        formatted_date = tarih.strftime("%Y-%m-%d")
        return await self._client.get(
            f"ibb/halfiyatlari/sebzemeyve/{formatted_date}",
            response_model=HalFiyatResponse,
        )
