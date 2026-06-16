from pydantic import BaseModel, Field

from izmir_open_data.endpoints.base import BaseEndpoint


class IzmirimKartDolumNoktasi(BaseModel):
    """
    İzmirimKart dolum noktası bilgisi (CSV datasından)
    Dolum noktalarının adres ve konum bilgilerini içerir
    """

    address: str = Field(alias="ADDRESS", description="Dolum noktası adresi")
    longitude: float | str = Field(alias="LONGITUDE", description="Boylam (longitude)")
    latitude: float | str = Field(alias="LATITUDE", description="Enlem (latitude)")


class IzmirimKartEndpoint(BaseEndpoint):
    async def get_dolum_noktalari(self) -> list[IzmirimKartDolumNoktasi]:
        """
        İzmirimKart dolum noktalarının adres ve konum bilgilerini içeren web servisi (CSV).

        Kaynak: https://acikveri.bizizmir.com/dataset/izmirimkart-dolum-noktalari
        """
        return await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/a0bb148a-f1f0-4a68-a534-4a273573d132/resource/7a3efbec-fa4f-4b1e-9f9a-ac28f3608b40/download/izmirimkart-dolum-noktalari.csv"
        )
