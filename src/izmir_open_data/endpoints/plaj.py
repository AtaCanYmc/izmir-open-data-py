from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class Plaj(DefaultOnemliYer):
    pass


class PlajEndpoint(BaseEndpoint):
    async def get_plajlar_list(self) -> OnemliYerWrapper[Plaj]:
        """
        Plajlar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/plajlar
        """
        return await self._client.get(
            "ibb/cbs/plajlar", response_model=OnemliYerWrapper[Plaj]
        )

    async def get_hamamlar_list(self) -> OnemliYerWrapper[Plaj]:
        """
        Hamamlar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/hamamlar
        """
        return await self._client.get(
            "ibb/cbs/hamamlar", response_model=OnemliYerWrapper[Plaj]
        )

    async def get_kaplicalar_list(self) -> OnemliYerWrapper[Plaj]:
        """
        Kaplıcalar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kaplicalar
        """
        return await self._client.get(
            "ibb/cbs/kaplicalar", response_model=OnemliYerWrapper[Plaj]
        )

    async def get_fuar_list(self) -> OnemliYerWrapper[Plaj]:
        """
        Fuar alanları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/fuar
        """
        return await self._client.get(
            "ibb/cbs/fuar", response_model=OnemliYerWrapper[Plaj]
        )
