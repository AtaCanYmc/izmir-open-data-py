from pydantic import BaseModel

from izmir_open_data.endpoints.base import BaseEndpoint


class AskidaIzmirimKartIstatistik(BaseModel):
    """
    Askıda İzmirim Kart istatistik bilgileri
    """
    AskidaBekleyenKart: int
    AskidanAlinanKart: int
    ToplamOdenenTutar: float

class IztekEndpoint(BaseEndpoint):
    async def get_askida_izmirim_kart_istatistik(self) -> AskidaIzmirimKartIstatistik:
        """
        Askıda İzmirim Kart istatistiklerini içeren web servisi.
        Askıda bekleyen kart sayısı, alınan kart sayısı ve toplam ödenen tutar bilgilerini döner.

        Kaynak: https://openapi.izmir.bel.tr/api/iztek/askidaizmirimkart
        """
        response = await self._client.get("iztek/askidaizmirimkart")
        return AskidaIzmirimKartIstatistik.model_validate(response)
