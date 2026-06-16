from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class Muhtarlik(DefaultOnemliYer):
    pass


class MuhtarliklarEndpoint(BaseEndpoint):
    async def get_list(self) -> OnemliYerWrapper[Muhtarlik]:
        """
        Muhtarlıklar hakkında bilgi ve coğrafi konumlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/muhtarliklar
        """
        response = await self._client.get("ibb/cbs/muhtarliklar")
        return OnemliYerWrapper[Muhtarlik].model_validate(response)
