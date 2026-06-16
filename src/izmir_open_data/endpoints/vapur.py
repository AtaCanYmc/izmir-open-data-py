from typing import Any

from pydantic import BaseModel

from src.izmir_open_data.endpoints.base import BaseEndpoint


class VapurSeferSaati(BaseModel):
    KalkisSaati: str | None = None
    VarisSaati: str | None = None

class VapurSeferSatiri(BaseModel):
    seferSaatleri: list[VapurSeferSaati]
    IptalMi: bool
    IptalAciklama: str
    Aciklama: str

class VapurHatti(BaseModel):
    hatAdi: str
    iskeleler: list[str]
    seferSatirlari: list[VapurSeferSatiri]

class VapurVarisYeri(BaseModel):
    iskeleAdi: str

class DetayliVapurSeferi(BaseModel):
    arabaliVapurSeferi: bool
    KalkisSaati: str
    VarisYerleri: list[VapurVarisYeri]
    Aciklama: str
    IptalMi: bool | None = None
    IptalAciklama: str | None = None

class GunlukVapurPlani(BaseModel):
    gunId: int
    seferler: list[DetayliVapurSeferi]

class VapurIskele(BaseModel):
    IskeleId: int
    Adi: str
    Enlem: float
    Boylam: float
    AktifMi: bool
    ArabaliVapurIskelesiMi: bool

class VapurDetay(BaseModel):
    """
    Vapur detay bilgisi (CSV datasından)
    Gemilerin kapasite ve donanım özellikleri
    """
    GEMI_ADI: str
    GEMI_TIPI: str
    YOLCU_KAPASITESI: int | str
    ARAC_KAPASITESI: int | str
    BISIKLET_PARK_YERI_KAPASITESI: int | str
    ENGELLI_ERISIMINE_UYGUNLUK: str
    ENGELLI_ASANSORU_SAYISI: int | str
    ERKEK_TUVALETI_SAYISI: int | str
    KADIN_TUVALETI_SAYISI: int | str
    ENGELLI_TUVALETI_SAYISI: int | str
    BEBEK_BAKIM_ODASI_SAYISI: int | str
    BUFE_VEYA_OTOMAT: str
    EVCIL_HAYVAN_TASIMA_KAFESI_SAYISI: int | str
    WIZMIRNET_KABLOSUZ_INTERNET: str

class VapurEndpoint(BaseEndpoint):
    async def get_hareket_saatleri(self, kalkis: str, varis: str, gun_tipi: int, detay: int = 0) -> Any:
        """
        Vapur hareket saatleri bilgisini içeren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/vapur-hareket-saatleri
        """
        return await self._client.get(f"izdeniz/vapursaatleri/{kalkis}/{varis}/{gun_tipi}/{detay}")

    async def get_calisma_gunleri(self) -> Any:
        """
        Vapurların çalışma günlerini içeren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/vapur-hareket-saatleri
        """
        return await self._client.get("izdeniz/gunler")

    async def get_hareket_saatleri_by_hat(self, iskele_id: str, gun_id: int) -> list[VapurHatti]:
        """
        İskele bazlı vapur hareket saatleri bilgisini içeren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/vapur-hareket-saatleri
        """
        return await self._client.get(f"izdeniz/iskelesefersaatleri/{iskele_id}/{gun_id}")

    async def get_iskele_list(self) -> list[VapurIskele]:
        """
        Vapur ve arabalı vapur iskele bilgilerini içeren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/izdeniz-vapur-iskeleleri
        """
        return await self._client.get("izdeniz/iskeleler")

    async def get_detay_list(self) -> list[VapurDetay]:
        """
        Vapurların detaylı bilgilerini içeren web servisi (CSV).
        Kapasite, donanım ve erişilebilirlik bilgilerini içerir (~20 gemi).
        Kaynak: https://acikveri.bizizmir.com/dataset/vapur-detay
        """
        return await self._client.get_csv(
            'https://acikveri.bizizmir.com/dataset/87b38b23-4f73-4650-9d96-c72ad6ee73e3/resource/e6d7425a-694c-4f39-b452-4aade132635c/download/vapurdetay.csv'
        )
