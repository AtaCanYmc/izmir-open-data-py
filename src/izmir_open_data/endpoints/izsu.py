from pydantic import BaseModel, Field

from izmir_open_data.endpoints.base import BaseEndpoint


class SuUretimi(BaseModel):
    uretim_kaynagi: str = Field(alias="UretimKaynagi")
    uretim_miktari: float = Field(alias="UretimMiktari")
    yil: int = Field(alias="Yil")
    ay: int = Field(alias="Ay")


class BarajKuyuUretim(BaseModel):
    tur_adi: str = Field(alias="TurAdi")
    baraj_kuyu_adi: str = Field(alias="BarajKuyuAdi")
    baraj_kuyu_id: int = Field(alias="BarajKuyuId")
    uretim_miktari: float = Field(alias="UretimMiktari")


class GunlukUretimResponse(BaseModel):
    uretim_tarihi: str = Field(alias="UretimTarihi")
    baraj_kuyu_uretimleri: list[BarajKuyuUretim] = Field(alias="BarajKuyuUretimleri")


class SuKaynagi(BaseModel):
    adi: str = Field(alias="Adi")
    enlem: float | None = Field(alias="Enlem", default=None)
    boylam: float | None = Field(alias="Boylam", default=None)
    tur_adi: str = Field(alias="TurAdi")


class BarajSuDurumu(BaseModel):
    su_durumu: float = Field(alias="SuDurumu")
    baraj_kuyu_adi: str = Field(alias="BarajKuyuAdi")
    su_yuksekligi: float = Field(alias="SuYuksekligi")
    kullanilabilir_gol_su_hacmi: float = Field(alias="KullanılabilirGolSuHacmi")
    boylam: float | None = Field(alias="Boylam", default=None)
    tuketilebilir_su_kapasitesi: float = Field(alias="TuketilebilirSuKapasitesi")
    maksimum_su_kapasitesi: float = Field(alias="MaksimumSuKapasitesi")
    baraj_su_durumu_gosterimi: str | None = Field(
        alias="BarajSuDurumuGosterimi", default=None
    )
    minimum_su_yuksekligi: float = Field(alias="MinimumSuYuksekligi")
    doluluk_orani: float = Field(alias="DolulukOrani")
    durum_tarihi: str = Field(alias="DurumTarihi")
    minimum_su_kapasitesi: float = Field(alias="MinimumSuKapasitesi")
    enlem: float | None = Field(alias="Enlem", default=None)
    baraj_kuyu_id: int = Field(alias="BarajKuyuId")
    maksimum_su_yuksekligi: float = Field(alias="MaksimumSuYuksekligi")


class SuAnalizSonucu(BaseModel):
    parametre_kodu: str = Field(alias="ParametreKodu")
    parametre_adi: str = Field(alias="ParametreAdi")
    birim: str = Field(alias="Birim")
    standart: str = Field(alias="Standart")
    parametre_degeri: str = Field(alias="ParametreDegeri")
    sonuc_id: int = Field(alias="SonucId")
    sonuc_tarihi: str = Field(alias="SonucTarihi")
    nokta_kodu: str = Field(alias="NoktaKodu")


class SuAnalizKaydi(BaseModel):
    tarih: str = Field(alias="Tarih")
    nokta_tanimi: str = Field(alias="NoktaTanimi")
    analiz_sonuclari: list[SuAnalizSonucu] = Field(alias="analizSonuclari")


class SuAnalizResponse(BaseModel):
    tum_analizler: list[SuAnalizKaydi] = Field(alias="TumAnalizler")


class BarajKaliteAnalizi(BaseModel):
    parametre_adi: str = Field(alias="ParametreAdi")
    standart: str = Field(alias="Standart")
    birim: str = Field(alias="Birim")
    islenmis_su: str = Field(alias="IslenmisSu")
    islenmemis_su: str = Field(alias="IslenmemisSu")
    regulasyon: str | None = Field(alias="Regulasyon", default=None)


class BarajAnalizGrubu(BaseModel):
    analiz_elemanlari: list[BarajKaliteAnalizi] = Field(alias="AnalizElemanlari")


class BarajAnalizKaydi(BaseModel):
    tarih: str = Field(alias="Tarih")
    analizler: list[BarajAnalizGrubu] = Field(alias="Analizler")


class BarajAnalizResponse(BaseModel):
    baraj_analizleri: list[BarajAnalizKaydi] = Field(alias="BarajAnalizleri")


class KesintiBilgisi(BaseModel):
    kesinti_tarihi: str = Field(alias="KesintiTarihi")
    aciklama: str = Field(alias="Aciklama")
    ilce_adi: str = Field(alias="IlceAdi")
    mahalle_id: list[int] = Field(alias="MahalleID")
    mahalleler: str = Field(alias="Mahalleler")
    tip: str = Field(alias="Tip")
    ariza_giderilme_tarihi: str = Field(alias="ArizaGiderilmeTarihi")
    ilce_id: int = Field(alias="IlceID")
    birim: str = Field(alias="Birim")
    ariza_id: int = Field(alias="ArizaID")
    ariza_durumu: str = Field(alias="ArizaDurumu")
    guncelleme_tarihi: str = Field(alias="GuncellemeTarihi")
    ariza_tip_id: int = Field(alias="ArizaTipID")
    kayit_tarihi: str = Field(alias="KayitTarihi")
    kesinti_suresi: str = Field(alias="KesintiSuresi")
    ongoru: str = Field(alias="Ongoru")


class IzsuSubeBilgisi(BaseModel):
    aktif_mi: bool = Field(alias="AktifMi")
    sube_adresi: str = Field(alias="SubeAdresi")
    enlem: str = Field(alias="ENLEM")
    boylam: str = Field(alias="BOYLAM")
    iletisim_durumu: bool = Field(alias="IletisimDurumu")
    sube_adi: str = Field(alias="SubeAdi")
    sube_telefon: str = Field(alias="SubeTelefon")


class IzsuVezneBilgisi(BaseModel):
    vezne_adi: str = Field(alias="VezneAdi")
    vezne_adresi: str | None = Field(alias="VezneAdresi", default=None)
    enlem: str | None = Field(alias="ENLEM", default=None)
    boylam: str | None = Field(alias="BOYLAM", default=None)
    aktif_mi: bool = Field(alias="AktifMi")
    bolge: str = Field(alias="Bolge")


class IzsuEndpoint(BaseEndpoint):
    async def get_su_uretimi_dagilimi(self) -> list[SuUretimi]:
        """
        Su üretiminin aylara ve kaynaklara göre dağılımını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/su-uretiminin-aylara-ve-kaynaklara-gore-dagilimi
        """
        return await self._client.get("izsu/suuretiminindagilimi")

    async def get_gunluk_su_uretimi(self) -> GunlukUretimResponse:
        """
        Günlük su üretimi miktarlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/gunluk-su-uretimi-miktarlari
        """
        return await self._client.get("izsu/gunluksuuretimi")

    async def get_baraj_doluluk_oranlari(self) -> list[BarajSuDurumu]:
        """
        Barajların doluluk oranlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/barajlarin-doluluk-oranlari
        """
        return await self._client.get("izsu/barajdurum")

    async def get_haftalik_su_analizi(self) -> SuAnalizResponse:
        """
        Güncel haftalık analiz sonuçlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/haftalik-analiz-sonuclari
        """
        return await self._client.get("izsu/haftaliksuanalizleri")

    async def get_baraj_su_kalite_raporlari(self) -> BarajAnalizResponse:
        """
        Baraj su kalite raporlarını içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/baraj-su-kalite-raporlari
        """
        return await self._client.get("izsu/barajsukaliteraporlari")

    async def get_ariza_kaynakli_kesinti_list(self) -> list[KesintiBilgisi]:
        """
        Arıza kaynaklı düzensiz su kesintilerinin ilçe, mahalle, kesinti süresi, sebebi ve açıklama verilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/ariza-kaynakli-duzensiz-su-kesintileri
        """
        return await self._client.get("izsu/arizakaynaklisukesintileri")

    async def get_baraj_ve_kuyu_list(self) -> list[SuKaynagi]:
        """
        Baraj ve kuyuların listesi ve konum bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/baraj-ve-kuyular
        """
        return await self._client.get("izsu/barajvekuyular")

    async def get_izsu_sube_list(self) -> list[IzsuSubeBilgisi]:
        """
        Şube adresleri, telefonları ve konum bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izsu-sube-ve-vezne-bilgileri
        """
        return await self._client.get("izsu/subeler")

    async def get_izsu_vezne_list(self) -> list[IzsuVezneBilgisi]:
        """
        Vezne adresleri, telefonları ve konum bilgilerini içeren web servisi.

        Kaynak: https://acikveri.bizizmir.com/dataset/izsu-sube-ve-vezne-bilgileri
        """
        return await self._client.get("izsu/vezneler")
