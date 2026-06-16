from src.izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from src.izmir_open_data.endpoints.base import BaseEndpoint


class BisimIstasyon(DefaultOnemliYer):
    pass


class BisimEndpoint(BaseEndpoint):
    async def get_istasyon_list(self) -> OnemliYerWrapper[BisimIstasyon]:
        """
        İstasyonların konum, kapasite ve bisiklet sayılarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/bisim-istasyonlari
        """
        return await self._client.get("izulas/bisim/istasyonlar")
