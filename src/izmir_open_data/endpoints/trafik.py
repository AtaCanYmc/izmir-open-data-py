
from pydantic import BaseModel

from src.izmir_open_data.endpoints.base import BaseEndpoint


class TrafikKamerasi(BaseModel):
    """
    Trafik kamerası bilgisi (CSV datasından)
    """
    ADI: str
    ENLEM: float
    BOYLAM: float

class TrafikEndpoint(BaseEndpoint):
    async def get_kamera_list(self) -> list[TrafikKamerasi]:
        """
        İzmir'deki trafik kameralarının listesini içeren web servisi (CSV).
        Kavşak adı ve koordinat bilgilerini içerir (~92 kamera).

        Kaynak: https://acikveri.bizizmir.com/dataset/trafik-kameralari
        """
        return await self._client.get_csv(
            'https://acikveri.bizizmir.com/dataset/a5cda2f2-ccbd-4fac-a4bb-c691abff28f1/resource/b91cb15d-05c6-45b7-8a75-48e030aad368/download/trafikkameralari.csv'
        )
