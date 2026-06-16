
from pydantic import BaseModel

from izmir_open_data.endpoints.base import BaseEndpoint


class MetroIstasyonu(BaseModel):
    IstasyonId: int
    Adi: str
    Enlem: float
    Boylam: float
    AktifMi: bool
    Sira: int

class MetroDurakMesafesi(BaseModel):
    """
    Metro durak mesafeleri bilgisi (CSV datasından)
    İstasyonlar arası mesafe bilgilerini içerir
    """
    ISTASYON_ID: int | str
    ISTASYON_ADI: str
    ISTASYON_SIRASI: int | str
    MESAFE: float | int | str

class MetroEndpoint(BaseEndpoint):
    async def get_istasyon_list(self) -> list[MetroIstasyonu]:
        """
        Metro istasyonları sıra ve konum verisi bilgileri içeren web servis.

        Kaynak: https://acikveri.bizizmir.com/dataset/metro-istayonlari
        """
        response = await self._client.get("metro/istasyonlar")
        return [MetroIstasyonu.model_validate(item) for item in response]

    async def get_durak_mesafeleri(self) -> list[MetroDurakMesafesi]:
        """
        Metro istasyonları arasındaki mesafe bilgilerini içeren web servisi (CSV).
        Her istasyonun bir önceki istasyona olan mesafesini metre cinsinden içerir.

        Kaynak: https://acikveri.bizizmir.com/dataset/metro-durak-mesafeleri
        """
        response = await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/b43d973e-8b98-4572-a944-dc39373ab7cb/resource/9a503344-25d5-4f34-8811-65e3108303ca/download/metro-durak-mesafeleri.csv",
            delimiter=","
        )
        return [MetroDurakMesafesi.model_validate(item) for item in response]
