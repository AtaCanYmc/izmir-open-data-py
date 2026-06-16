from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class UlasimNoktasi(DefaultOnemliYer):
    """Ulaşım noktası için interface"""
    pass

class TrenEndpoint(BaseEndpoint):
    async def get_tren_garlari_list(self) -> OnemliYerWrapper[UlasimNoktasi]:
        """
        Tren garları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/trengarlari
        """
        return await self._client.get("ibb/cbs/trengarlari")

    async def get_havaalani_list(self) -> OnemliYerWrapper[UlasimNoktasi]:
        """
        Havaalanı konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/havaalani
        """
        return await self._client.get("ibb/cbs/havaalani")

    async def get_otobus_terminalleri_list(self) -> OnemliYerWrapper[UlasimNoktasi]:
        """
        Şehirlerarası otobüs terminalleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/otobusterminalleri
        """
        return await self._client.get("ibb/cbs/otobusterminalleri")

    async def get_arac_muayene_istasyonlari_list(self) -> OnemliYerWrapper[UlasimNoktasi]:
        """
        Araç muayene istasyonları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/aracmuayeneistasyonlari
        """
        return await self._client.get("ibb/cbs/aracmuayeneistasyonlari")
