from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class SosyalHizmetMerkezi(DefaultOnemliYer):
    pass


class SosyalEndpoint(BaseEndpoint):
    async def get_aile_dayanisma_merkezleri_list(
        self,
    ) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Aile dayanışma merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ailedayanismamerkezleri
        """
        return await self._client.get(
            "ibb/cbs/ailedayanismamerkezleri",
            response_model=OnemliYerWrapper[SosyalHizmetMerkezi],
        )

    async def get_cocuk_genclik_merkezleri_list(
        self,
    ) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Çocuk ve gençlik merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/cocukvegenclikmerkezleri
        """
        return await self._client.get(
            "ibb/cbs/cocukvegenclikmerkezleri",
            response_model=OnemliYerWrapper[SosyalHizmetMerkezi],
        )

    async def get_cocuk_yuvalari_list(self) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Çocuk yuvaları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/cocukyuvalari
        """
        return await self._client.get(
            "ibb/cbs/cocukyuvalari",
            response_model=OnemliYerWrapper[SosyalHizmetMerkezi],
        )

    async def get_huzurevleri_list(self) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Huzurevleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/huzurevleri
        """
        return await self._client.get(
            "ibb/cbs/huzurevleri", response_model=OnemliYerWrapper[SosyalHizmetMerkezi]
        )

    async def get_toplum_merkezleri_list(self) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Toplum merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/toplummerkezleri
        """
        return await self._client.get(
            "ibb/cbs/toplummerkezleri",
            response_model=OnemliYerWrapper[SosyalHizmetMerkezi],
        )

    async def get_yetistirme_yurtlari_list(
        self,
    ) -> OnemliYerWrapper[SosyalHizmetMerkezi]:
        """
        Yetiştirme yurtları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/yetistirmeyurtlari
        """
        return await self._client.get(
            "ibb/cbs/yetistirmeyurtlari",
            response_model=OnemliYerWrapper[SosyalHizmetMerkezi],
        )
