
from pydantic import BaseModel

from src.izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from src.izmir_open_data.endpoints.base import BaseEndpoint


class SporTesisi(DefaultOnemliYer):
    pass


class YuruyusYolu(BaseModel):
    """
    Yürüyüş yolu/parkur bilgisi (CSV datasından)
    """

    PARKUR: str
    YURUYUS: str
    MESAFE: float | str
    MINIMUM_YUKSEKLIK: float | str
    MAKSIMUM_YUKSEKLIK: float | str
    ZAMAN: float | str
    ZORLUK_DERECESI: str
    BISIKLET: str


class SporEndpoint(BaseEndpoint):
    """
    Spor tesisleri endpoint'leri.
    NOT: Bu endpoint'ler PDF dokümantasyonunda belirtilmiş ancak
    API'de henüz aktif değil (404 dönüyor). İleride aktif olabilir.
    """

    async def get_hipodrom_list(self) -> OnemliYerWrapper[SporTesisi]:
        """
        Hipodrom konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/hipodrom
        @deprecated API'de henüz aktif değil
        """
        return await self._client.get(
            "ibb/cbs/hipodrom", response_model=OnemliYerWrapper[SporTesisi]
        )

    async def get_spor_salonlari_list(self) -> OnemliYerWrapper[SporTesisi]:
        """
        Spor salonları ve sahaları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/sporsalonlari
        @deprecated API'de henüz aktif değil
        """
        return await self._client.get(
            "ibb/cbs/sporsalonlari", response_model=OnemliYerWrapper[SporTesisi]
        )

    async def get_stadyumlar_list(self) -> OnemliYerWrapper[SporTesisi]:
        """
        Stadyumlar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/stadyumlar
        @deprecated API'de henüz aktif değil
        """
        return await self._client.get(
            "ibb/cbs/stadyumlar", response_model=OnemliYerWrapper[SporTesisi]
        )

    async def get_yuruyus_yollari(self) -> list[YuruyusYolu]:
        """
        Yürüyüş ve bisiklet parkurlarının bilgilerini içeren web servisi (CSV).
        Parkur adı, mesafe, yükseklik, zorluk derecesi gibi bilgileri içerir.

        Kaynak: https://acikveri.bizizmir.com/dataset/yuruyus-yollari
        """
        return await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/48fa21a3-b286-40f2-a286-28aa9dc328df/resource/4896beb8-0139-4135-9475-d790c18bbb19/download/yuruyus-yollar.csv",
            response_model=YuruyusYolu,
        )
