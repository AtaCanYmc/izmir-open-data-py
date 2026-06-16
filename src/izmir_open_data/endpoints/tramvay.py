from typing import Literal

from pydantic import BaseModel

from izmir_open_data.endpoints.base import BaseEndpoint


class TramvayHatti(BaseModel):
    HatId: int
    Adi: str
    Aciklama: str
    HatBaslangic: str
    HatBitis: str


class TramvayIstasyonu(BaseModel):
    IstasyonId: int
    Adi: str
    Enlem: float
    Boylam: float


class TramvaySeferSikligi(BaseModel):
    Sira: int
    BaslangicSaati: str
    BitisSaati: str
    Aralik: int
    TarifeId: int
    SeferId: int


class TramvaySefer(BaseModel):
    BaslangicSaati: str
    BitisSaati: str
    Aralik: int


class TramvayPlanlananiSefer(BaseModel):
    """
    Planlanan sefer sayıları (CSV datasından)
    Metro ve tramvay hatları için aylık planlanan sefer sayıları
    """

    YIL: int
    AY: int
    IZMIR_METROSU: int
    KARSIYAKA_TRAMVAYI_VE_CIGLI_TRAMVAYI: int
    KONAK_TRAMVAYI: int


class TramvayDurakMesafesi(BaseModel):
    """
    Tramvay durak mesafeleri bilgisi (CSV datasından)
    İstasyonlar arası mesafe bilgilerini içerir
    """

    ISTASYON_ID: int | str
    ISTASYON_ADI: str
    ISTASYON_SIRASI: int | str
    MESAFE: int | str


TramvayHatTipi = Literal["karsiyaka", "konak-sag", "konak-sol", "cigili"]

TRAMVAY_DURAK_MESAFE_URLS = {
    "karsiyaka": "https://acikveri.bizizmir.com/dataset/b43d973e-8b98-4572-a944-dc39373ab7cb/resource/45d03ae3-f928-441f-bed3-e26c5edd9f42/download/tramvay-karsiyaka-durak-mesafeleri.csv",
    "konak-sag": "https://acikveri.bizizmir.com/dataset/b43d973e-8b98-4572-a944-dc39373ab7cb/resource/32930780-fd3a-4b9d-a1b5-a299440a1d6c/download/tramvay-konak-durak-mesafeleri-sag.csv",
    "konak-sol": "https://acikveri.bizizmir.com/dataset/b43d973e-8b98-4572-a944-dc39373ab7cb/resource/33480acc-873b-43e5-aa3d-2bd6d5fb2134/download/tramvay-konak-durak-mesafeleri-sol.csv",
    "cigili": "https://acikveri.bizizmir.com/dataset/b43d973e-8b98-4572-a944-dc39373ab7cb/resource/b29426e4-39ae-4b89-8bbd-be6104161fb7/download/tramvay-cigili-durak-mesafeleri.csv",
}


class TramvayEndpoint(BaseEndpoint):
    async def get_hat_list(self) -> list[TramvayHatti]:
        """
        Tramvay hatları bilgisini içeren web servis:
        Kaynak: https://acikveri.bizizmir.com/dataset/izmir-tramvay-hatlari-ve-istasyonlari
        """
        return await self._client.get("tramvay/hatlar")

    async def get_sefer_list(self) -> list[TramvaySefer]:
        """
        Tüm tramvay sefer bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/tramvay/sefer
        """
        return await self._client.get("tramvay/sefer")

    async def get_istasyon_list(self, sefer_id: int) -> list[TramvayIstasyonu]:
        """
        Sefer numarasına göre tramvay istasyonları listesini içeren web servis.
        Kaynak: https://acikveri.bizizmir.com/dataset/izmir-tramvay-hatlari-ve-istasyonlari
        """
        return await self._client.get(f"tramvay/istasyonlar/{sefer_id}")

    async def get_sefer_siklik_list(self, sefer_id: int) -> list[TramvaySeferSikligi]:
        """
        Sefer numarasına göre tramvay sefer sıklıkları bilgisini veren web servisi.
        Kaynak: https://acikveri.bizizmir.com/dataset/tramvay-seferleri
        """
        return await self._client.get(f"tramvay/seferler/{sefer_id}")

    async def get_planlanani_sefer_sayilari(self) -> list[TramvayPlanlananiSefer]:
        """
        Metro ve tramvay hatları için aylık planlanan sefer sayılarını içeren web servisi (CSV).
        İzmir Metrosu, Karşıyaka/Çiğli Tramvayı ve Konak Tramvayı verilerini içerir.
        Kaynak: https://acikveri.bizizmir.com/dataset/planlanan-sefer-sayilari
        """
        return await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/ace45290-413e-4786-82e4-d23fd56591b1/resource/2fc4d0cf-9628-43b7-95d3-df5742a95f02/download/planlanan_sefer_sayilari.csv"
        )

    async def get_durak_mesafeleri(
        self, hat: TramvayHatTipi
    ) -> list[TramvayDurakMesafesi]:
        """
        Tramvay hatları için durak mesafelerini içeren web servisi (CSV).
        Her istasyonun bir önceki istasyona olan mesafesini metre cinsinden içerir.
        Kaynak: https://acikveri.bizizmir.com/dataset/tramvay-durak-mesafeleri
        """
        url = TRAMVAY_DURAK_MESAFE_URLS[hat]
        return await self._client.get_csv(url)
