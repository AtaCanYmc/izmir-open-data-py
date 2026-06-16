from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class TarihiYapi(DefaultOnemliYer):
    """Tarihi yapılar için interface"""
    pass

class TarihiEndpoint(BaseEndpoint):
    async def get_antik_kentler_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Antik kentler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/antikkentler
        """
        return await self._client.get("ibb/cbs/antikkentler")

    async def get_antik_kent_yapilari_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Antik kent yapıları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/antikkentyapilari
        """
        return await self._client.get("ibb/cbs/antikkentyapilari")

    async def get_kosk_ve_konaklar_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Köşk ve konaklar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/koskvekonaklar
        """
        return await self._client.get("ibb/cbs/koskvekonaklar")

    async def get_kule_anit_heykeller_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Kule, anıt ve heykeller konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kuleanitveheykeller
        """
        return await self._client.get("ibb/cbs/kuleanitveheykeller")

    async def get_tarihi_carsi_hanlar_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Tarihi çarşı ve hanlar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/tarihicarsivehanlar
        """
        return await self._client.get("ibb/cbs/tarihicarsivehanlar")

    async def get_tarihi_su_yapilari_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Tarihi su yapıları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/tarihisuyapilari
        """
        return await self._client.get("ibb/cbs/tarihisuyapilari")

    async def get_tarihi_yapilar_list(self) -> OnemliYerWrapper[TarihiYapi]:
        """
        Tarihi yapılar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/tarihiyapilar
        """
        return await self._client.get("ibb/cbs/tarihiyapilar")
