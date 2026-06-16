from typing import Any, Literal

from pydantic import BaseModel, Field

from izmir_open_data.endpoints.base import BaseEndpoint


class OccupancyTotal(BaseModel):
    free: int
    occupied: int


class OccupancyDisabled(BaseModel):
    free: int
    occupied: int


class Occupancy(BaseModel):
    total: OccupancyTotal
    disabled: OccupancyDisabled | None = None


class Accessibility(BaseModel):
    lpgAllowed: bool
    disabled: bool
    maxLength: float
    maxHeight: float
    maxWidth: float


class Poi(BaseModel):
    metroStation: bool
    trainStation: bool
    busStation: bool
    tramStation: bool


class Payment(BaseModel):
    cash: bool
    card: bool
    sms: bool


class Accessories(BaseModel):
    covered: bool
    barrier: bool
    cctv: bool


class OtoparkBilgisi(BaseModel):
    ufid: str
    name: str
    status: Literal["Closed", "Opened"]
    type: Literal["OnStreet", "OffStreet"]
    provider: str
    lat: float
    lng: float
    isPaid: bool
    nonstop: bool
    openingHours: dict[str, str]
    occupancy: Occupancy
    accessibility: Accessibility
    poi: Poi
    payment: Payment
    accessories: Accessories


class OtoparkUcreti(BaseModel):
    """İzelman otopark ücret bilgisi (CKAN datasından)"""

    id: int = Field(alias="_id")
    otopark_fiyat: str = Field(alias="Otopark / Fiyat")
    saat_0_1: float | None = Field(None, alias="0-1 Saat")
    saat_0_2: float | None = Field(None, alias="0-2 saat")
    saat_2_4: float | None = Field(None, alias="2-4 saat")
    saat_4_6: float | None = Field(None, alias="4-6 saat")
    saat_0_3: str | None = Field(None, alias="0-3 saat")
    saat_0_6: float | None = Field(None, alias="0-6 saat")
    saat_3_6: str | None = Field(None, alias="3-6 saat")
    saat_6_12: float | None = Field(None, alias="6-12 saat")
    saat_1_12: float | None = Field(None, alias="1-12 saat")
    saat_0_12: float | None = Field(None, alias="0-12 saat")
    saat_12_24: float | None = Field(None, alias="12-24 saat")
    saat_0_24: float | None = Field(None, alias="0-24 saat")
    motosiklet_0_12: float | None = Field(None, alias="0-12 Saat(Motosiklet )")
    motosiklet_12_24: float | None = Field(None, alias="12-24 Saat(Motosiklet )")
    motosiklet_0_24: float | None = Field(None, alias="0-24 Saat(Motosiklet )")
    kayip_bilet: float | None = Field(None, alias="Kayıp Bilet")
    aylik_abone: float | None = Field(None, alias="Aylık Abone Ücreti")
    aylik_alan_abone: float | None = Field(None, alias="Aylık Alan Abonelik Ücreti")
    motosiklet_aylik_abone: float | None = Field(
        None, alias="Motosiklet Aylık Abone Ücreti"
    )
    engelli_0_12: float | None = Field(None, alias="0-12 Saat(Engelli Aracı )")
    engelli_12_24: float | None = Field(None, alias="12-24 Saat(Engelli Aracı )")
    engelli_0_24: float | None = Field(None, alias="0-24 Saat(Engelli Aracı )")


class OtoparkEndpoint(BaseEndpoint):
    async def get_list(self) -> list[OtoparkBilgisi]:
        """
        Otoparkların konumu, dolu-boş adetleri, çalışma saatleri bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/otopark-doluluk-ve-lokasyon-bilgileri
        """
        response = await self._client.get("izum/otoparklar")
        return [OtoparkBilgisi.model_validate(item) for item in response]

    async def get_ucretler(self, limit: int = 100, offset: int = 0) -> Any:
        """
        İzelman otopark ücretlerini içeren web servisi (CKAN).
        Her otopark için farklı saat dilimleri ve araç tiplerinin ücret bilgilerini içerir.

        Kaynak: https://acikveri.bizizmir.com/dataset/izelman-otopark-ucretleri
        """
        response = await self._client.get_ckan(
            "datastore_search",
            params={
                "resource_id": "b45d2e9f-f258-476e-a12d-d0ff62471ee0",
                "limit": limit,
                "offset": offset,
            },
        )
        return response
