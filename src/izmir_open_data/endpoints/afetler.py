from src.izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from src.izmir_open_data.endpoints.base import BaseEndpoint


class AfetToplanmaAlanlari(DefaultOnemliYer):
    pass


class AfetlerEndpoint(BaseEndpoint):
    async def get_acil_durum_toplanma_alanlari(self) -> OnemliYerWrapper[AfetToplanmaAlanlari]:
        """
        Afet ve acil durum toplanma alanlarına ait ilçe, mahalle ve konum bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/afet-ve-acil-durum-toplanma-alanlari
        """
        return await self._client.get("ibb/cbs/afetaciltoplanmaalani")
