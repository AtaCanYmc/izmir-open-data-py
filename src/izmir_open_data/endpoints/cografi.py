from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class CografiYer(DefaultOnemliYer):
    pass


class CografiEndpoint(BaseEndpoint):
    async def get_ada_yarimada_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Ada ve yarımada konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/adayarimada
        """
        return await self._client.get("ibb/cbs/adayarimada")

    async def get_burunlar_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Burun konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/burunlar
        """
        return await self._client.get("ibb/cbs/burunlar")

    async def get_dag_tepe_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Dağ ve tepelerin konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/dagtepe
        """
        return await self._client.get("ibb/cbs/dagtepe")

    async def get_goller_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Göl konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/goller
        """
        return await self._client.get("ibb/cbs/goller")

    async def get_korfez_koylar_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Körfez ve koyların konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/korfezvekoylar
        """
        return await self._client.get("ibb/cbs/korfezvekoylar")

    async def get_nehir_caylar_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Nehir ve çayların konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/nehirvecaylar
        """
        return await self._client.get("ibb/cbs/nehirvecaylar")

    async def get_ormanlar_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Ormanların konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ormanlar
        """
        return await self._client.get("ibb/cbs/ormanlar")

    async def get_meydanlar_list(self) -> OnemliYerWrapper[CografiYer]:
        """
        Meydanların konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/meydanlar
        """
        return await self._client.get("ibb/cbs/meydanlar")
