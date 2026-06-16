from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class KulturMekani(DefaultOnemliYer):
    pass

class KutuphaneEndpoint(BaseEndpoint):
    async def get_kutuphaneler_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Kütüphaneler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kutuphaneler
        """
        response = await self._client.get("ibb/cbs/kutuphaneler")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_kultur_merkezleri_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Kültür merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kulturmerkezleri
        """
        response = await self._client.get("ibb/cbs/kulturmerkezleri")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_opera_ve_bale_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Opera ve bale konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/operavebale
        """
        response = await self._client.get("ibb/cbs/operavebale")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_galeri_ve_salonlar_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Sanat galerisi ve sergi salonları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/galerivesalonlar
        """
        response = await self._client.get("ibb/cbs/galerivesalonlar")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_senfoni_orkestrasi_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Senfoni orkestrası konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/senfoniorkestrasi
        """
        response = await self._client.get("ibb/cbs/senfoniorkestrasi")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_sinemalar_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Sinemalar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/sinemalar
        """
        response = await self._client.get("ibb/cbs/sinemalar")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_tiyatrolar_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Tiyatrolar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/tiyatrolar
        """
        response = await self._client.get("ibb/cbs/tiyatrolar")
        return OnemliYerWrapper[KulturMekani].model_validate(response)

    async def get_muzeler_list(self) -> OnemliYerWrapper[KulturMekani]:
        """
        Müzeler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/muzeler
        """
        response = await self._client.get("ibb/cbs/muzeler")
        return OnemliYerWrapper[KulturMekani].model_validate(response)
