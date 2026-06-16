from typing import Literal

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel

from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class EshotDurak(DefaultOnemliYer):
    pass


class EshotHat(BaseModel):
    HAT_NO: int
    HAT_ADI: str
    GUZERGAH_ACIKLAMA: str
    ACIKLAMA: str
    HAT_BASLANGIC: str
    HAT_BITIS: str


class EshotHareketSaati(BaseModel):
    HAT_NO: int
    TARIFE_ID: int
    GIDIS_SAATI: str
    DONUS_SAATI: str
    SIRA: int
    GIDIS_ENGELLI_DESTEGI: str
    DONUS_ENGELLI_DESTEGI: str
    BISIKLETLI_GIDIS: str
    BISIKLETLI_DONUS: str
    GIDIS_ELEKTRIKLI_OTOBUS: str
    DONUS_ELEKTRIKLI_OTOBUS: str


class EshotDurakCSV(BaseModel):
    DURAK_ID: int
    DURAK_ADI: str
    ENLEM: float
    BOYLAM: float
    DURAKTAN_GECEN_HATLAR: str


class EshotHatGuzergah(BaseModel):
    HAT_NO: int
    YON: int
    BOYLAM: float
    ENLEM: float


class EshotBaglantiTipi(BaseModel):
    BAGLANTI_TIP_ID: int
    BAGLANTI_TIPI: str


class EshotBaglantiHat(BaseModel):
    BAGLANTI_TIP_ID: int
    HAT_NO: int
    HAT_ADI: str
    GUZERGAH_ACIKLAMA: str
    ACIKLAMA: str
    HAT_BASLANGIC: str
    HAT_BITIS: str
    GIDIS_CALISMA_SAATI: str
    DONUS_CALISMA_SAATI: str


class YaklasanOtobus(BaseModel):
    KalanDurakSayisi: int
    HattinYonu: int
    KoorY: float
    BisikletAparatliMi: bool
    KoorX: float
    EngelliMi: bool
    HatNumarasi: int
    HatAdi: str
    OtobusId: int


class EshotSiraliDurak(BaseModel):
    hatNo: str
    yon: int
    durakAdi: str
    durakId: str
    sira: int


class HatOtobusKonumlariResponse(BaseModel):
    HataMesaj: str
    HatOtobusKonumlari: list[YaklasanOtobus]


class EshotEndpoint(BaseEndpoint):
    async def get_hatlar(self) -> list[EshotHat]:
        """
        ESHOT hatlarının listesini içeren web servisi (CSV).
        Tüm hat verilerini tek seferde döndürür (~441 hat).

        Kaynak: https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hatlari.csv
        """
        return await self._client.get_csv('https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hatlari.csv')

    async def get_hareket_saatleri(self) -> list[EshotHareketSaati]:
        """
        ESHOT otobüs hareket saatlerini içeren web servisi (CSV).
        Tüm hareket saati verilerini tek seferde döndürür (~101,000+ kayıt).

        Kaynak: https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hareketsaatleri.csv
        """
        return await self._client.get_csv('https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hareketsaatleri.csv')

    async def get_duraklar(self) -> list[EshotDurakCSV]:
        """
        ESHOT otobüs duraklarının listesini içeren web servisi (CSV).
        Tüm durak verilerini tek seferde döndürür (~11,770 durak).

        Kaynak: https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-duraklari.csv
        """
        return await self._client.get_csv('https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-duraklari.csv')

    async def get_hat_guzergahlari(self) -> list[EshotHatGuzergah]:
        """
        ESHOT hat güzergahlarını içeren web servisi (CSV).
        Her hat için gidiş (YON=1) ve dönüş (YON=2) koordinat noktalarını içerir.
        Tüm güzergah verilerini tek seferde döndürür (~560,000+ nokta).

        Kaynak: https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hat-guzergahlari.csv
        """
        return await self._client.get_csv(
            'https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hat-guzergahlari.csv')

    async def get_baglanti_tipleri(self) -> list[EshotBaglantiTipi]:
        """
        Otobüs hatlarının diğer ulaşım araçları ile bağlantı tiplerini içeren web servisi (CSV).
        Metro, İzban, Vapur, Havaalanı, Otogar gibi bağlantı tiplerini listeler.

        Kaynak: https://acikveri.bizizmir.com/dataset/otobus-hatlarinin-diger-ulasim-araclari-ile-baglanti-tipleri
        """
        return await self._client.get_csv(
            'https://acikveri.bizizmir.com/dataset/f0964595-53e0-4b94-bf11-9423f8bb595e/resource/c228da75-adfd-422a-a480-2a4c7ffa7586/download/eshot-otobus-baglanti-tipleri.csv')

    async def get_baglanti_hatlari(self) -> list[EshotBaglantiHat]:
        """
        Diğer ulaşım araçları ile bağlantılı otobüs hatlarının listesini içeren web servisi (CSV).
        Her hattın hangi ulaşım aracına bağlantılı olduğunu ve çalışma saatlerini gösterir (~583 kayıt).

        Kaynak: https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-baglantili-hatlar.csv
        """
        return await self._client.get_csv(
            'https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-baglantili-hatlar.csv')

    async def get_yakin_durak_list(self, enlem: float, boylam: float) -> OnemliYerWrapper[EshotDurak]:
        """
        ESHOT duraklarının konum, isim ve diğer bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/eshot-duraklari
        """
        return await self._client.get(f"ibb/cbs/noktayayakinduraklar?x={enlem}&y={boylam}")

    async def get_duraga_yaklasan_otobus_list(self, durak_id: int) -> list[YaklasanOtobus]:
        """
        Bir durağa yaklaşan otobüslerin listesi, konumu ve diğer bilgilerini içeren web servisi.

        Kaynak: https://openapi.izmir.bel.tr/api/iztek/duragayaklasanotobusler/{durakId}
        :param durak_id: Durak numarası (ESHOT durak listesinden alınabilir)
        """
        return await self._client.get(f"iztek/duragayaklasanotobusler/{durak_id}")

    async def get_hattin_yaklasan_otobusleri(self, hat_id: int, durak_id: int) -> list[YaklasanOtobus]:
        """
        Bir hattın belirli bir durağa yaklaşan otobüslerinin konum ve diğer bilgilerini içeren web servisi.

        Kaynak: https://openapi.izmir.bel.tr/api/iztek/hattinyaklasanotobusleri/{hatId}/{durakId}
        :param hat_id: Hat numarası
        :param durak_id: Durak numarası
        """
        return await self._client.get(f"iztek/hattinyaklasanotobusleri/{hat_id}/{durak_id}")

    async def get_hat_otobus_konumlari(self, hat_id: int) -> HatOtobusKonumlariResponse:
        """
        Numarası girilen hatta ait otobüslerin anlık konum bilgilerini içeren web servisi.

        Kaynak: https://openapi.izmir.bel.tr/api/iztek/hatotobuskonumlari/{hatId}
        :param hat_id: Hat numarası
        """
        return await self._client.get(f"iztek/hatotobuskonumlari/{hat_id}")

    async def scrap_eshot_sirali_durak_listesi(self, hat_no: str, yon: Literal[0, 1]) -> list[EshotSiraliDurak]:
        """
        ESHOT duraklarının sıralı listesini çeken web servisi.

        Belirli bir hat numarası ve yön için durak listesini sıralı olarak döndürür.
        Gidiş için 0, dönüş için 1 değeri kullanılmalıdır.

        Kaynak: https://www.eshot.gov.tr/tr/UlasimSaatleri/{hatNo}/288
        :param hat_no: Hat numarası (ör: '390')
        :param yon: 0: Gidiş, 1: Dönüş
        :returns: Sıralı durak listesi
        """
        url = f"https://www.eshot.gov.tr/tr/UlasimSaatleri/{hat_no}/288"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    },
                    data={'hatYon': str(yon)}
                )
                response.raise_for_status()
                html = response.text

                soup = BeautifulSoup(html, 'html.parser')
                stops = []
                for block in soup.select('.block-transfer'):
                    ul = block.select_one('ul.transfer')
                    if ul:
                        stops = [li.text.strip() for li in ul.select('li.ring')]
                        if stops:
                            break

                result = []
                for idx, durak in enumerate(stops):
                    parts = durak.split(' - ')
                    result.append(EshotSiraliDurak(
                        hatNo=hat_no,
                        yon=yon,
                        durakAdi=parts[0] if len(parts) > 0 else "-",
                        durakId=parts[1] if len(parts) > 1 else "-",
                        sira=idx + 1
                    ))
                return result
        except Exception as e:
            print(f"ESHOT durakları çekilirken hata oluştu: {e}")
            return []
