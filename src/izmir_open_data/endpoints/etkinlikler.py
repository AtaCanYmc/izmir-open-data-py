
from pydantic import BaseModel, Field

from src.izmir_open_data.endpoints.base import BaseEndpoint


class IzmirEtkinlik(BaseModel):
    tur: str = Field(alias="Tur")
    id: int = Field(alias="Id")
    adi: str = Field(alias="Adi")
    etkinlik_bitis_tarihi: str = Field(alias="EtkinlikBitisTarihi")
    kucuk_afis: str = Field(alias="KucukAfis")
    etkinlik_merkezi: str = Field(alias="EtkinlikMerkezi")
    kisa_aciklama: str = Field(alias="KisaAciklama")
    bilet_satis_linki: str | None = Field(alias="BiletSatisLinki", default=None)
    ucretsiz_mi: bool = Field(alias="UcretsizMi")
    resim: str = Field(alias="Resim")
    etkinlik_url: str = Field(alias="EtkinlikUrl")
    etkinlik_baslama_tarihi: str = Field(alias="EtkinlikBaslamaTarihi")

class EtkinliklerEndpoint(BaseEndpoint):
    async def get_list(self) -> list[IzmirEtkinlik]:
        """
        Güncel kültür sanat etkinlikler listesini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/kultur-sanat-etkinlikleri
        """
        return await self._client.get("ibb/kultursanat/etkinlikler")

    async def get_etkinlik_by_id(self, etkinlik_id: int) -> IzmirEtkinlik:
        """
        Belirli bir etkinliğin detay bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/kultur-sanat-etkinlikleri
        """
        return await self._client.get(f"ibb/kultursanat/etkinlikler/{etkinlik_id}")
