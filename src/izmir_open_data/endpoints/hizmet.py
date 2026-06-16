from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class HizmetNoktasi(DefaultOnemliYer):
    pass

class HizmetEndpoint(BaseEndpoint):
    async def get_hizmet_nokta_list(self) -> OnemliYerWrapper[HizmetNoktasi]:
        """
        İzBB bünyesindeki hizmet noktalarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izbb-hizmet-noktalari
        """
        return await self._client.get("ibb/cbs/izbbhizmetnoktalari")
