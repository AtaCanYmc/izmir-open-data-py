from pydantic import BaseModel

from izmir_open_data.endpoints.base import BaseEndpoint


class Eczane(BaseModel):
    Adi: str
    Telefon: str
    Adres: str
    Bolge: str
    BolgeAciklama: str
    LokasyonX: str
    LokasyonY: str
    Tarih: str


class EczanelerEndpoint(BaseEndpoint):
    async def get_nobetci_list(self) -> list[Eczane]:
        """
        Nöbetçi eczanelerin bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/nobetci-eczaneler-ve-eczane-listesi
        """
        return await self._client.get("ibb/nobetcieczaneler")

    async def get_list(self) -> list[Eczane]:
        """
        Eczanelerin bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/nobetci-eczaneler-ve-eczane-listesi
        """
        return await self._client.get("ibb/eczaneler")
