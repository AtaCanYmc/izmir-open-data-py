from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class WizmirNetKonum(DefaultOnemliYer):
    """Ücretsiz-kablosuz internet hizmet noktaları ve lokasyon bilgilerini içeren web servisi."""

    pass


class WizmirnetEndpoint(BaseEndpoint):
    async def get_list(self) -> OnemliYerWrapper[WizmirNetKonum]:
        """
        Ücretsiz-kablosuz internet hizmet noktaları ve lokasyon bilgilerini içeren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/kablosuz-internet-baglanti-noktalari
        """
        return await self._client.get("ibb/cbs/wizmirnetnoktalari")
