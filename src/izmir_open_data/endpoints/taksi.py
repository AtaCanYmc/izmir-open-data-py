from src.izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from src.izmir_open_data.endpoints.base import BaseEndpoint


class TaksiDurak(DefaultOnemliYer):
    pass


class TaksiEndpoint(BaseEndpoint):
    async def get_durak_list(self) -> OnemliYerWrapper[TaksiDurak]:
        """
        Taksi durak bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/taksi-durak-bilgileri
        """
        return await self._client.get(
            "ibb/cbs/taksiduraklari", response_model=OnemliYerWrapper[TaksiDurak]
        )
