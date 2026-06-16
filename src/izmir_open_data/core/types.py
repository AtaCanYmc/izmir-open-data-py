from typing import Generic, TypeVar

from pydantic import AliasChoices, BaseModel, Field

T = TypeVar("T")


class DefaultOnemliYer(BaseModel):
    id: int | None = Field(None, alias="Id")
    adi: str | None = Field(None, alias="Adi")
    aciklama: str | None = Field(None, alias="Aciklama")
    boylam: float | None = Field(None, alias="Boylam")
    enlem: float | None = Field(None, alias="Enlem")
    ilce_id: int | None = Field(None, alias="IlceId")
    ilce_adi: str | None = Field(None, alias="IlceAdi")
    mahalle_id: int | None = Field(None, alias="MahalleId")
    mahalle_adi: str | None = Field(None, alias="MahalleAdi")
    kapi_no: str | None = Field(None, alias="KapiNo")
    telefon: str | None = Field(None, alias="Telefon")
    eposta: str | None = Field(None, alias="Eposta")
    web_adresi: str | None = Field(None, alias="WebAdresi")
    resim_url: str | None = Field(None, alias="ResimUrl")
    yol_tarifi_kisa: str | None = Field(None, alias="YolTarifiKisa")


class OnemliYerWrapper(BaseModel, Generic[T]):
    kayit_sayisi: int = Field(alias="kayit_sayisi")
    sayfa_numarasi: int = Field(alias="sayfa_numarasi")
    sayfa_basina_kayit_sayisi: int = Field(
        validation_alias=AliasChoices(
            "sayfa_basina_kayit_sayisi", "sayfadaki_kayitsayisi"
        )
    )
    toplam_sayfa_sayisi: int = Field(alias="toplam_sayfa_sayisi")
    kayitlar: list[T] = Field(validation_alias=AliasChoices("kayitlar", "onemliyer"))
