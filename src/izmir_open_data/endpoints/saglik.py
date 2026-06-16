from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class SaglikKurumu(DefaultOnemliYer):
    pass


class SaglikEndpoint(BaseEndpoint):
    async def get_acil_yardim_istasyonlari_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Acil yardım istasyonları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/acilyardimistasyonu
        """
        return await self._client.get(
            "ibb/cbs/acilyardimistasyonu", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_aile_sagligi_merkezleri_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Aile sağlığı merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ailesagligimerkezleri
        """
        return await self._client.get(
            "ibb/cbs/ailesagligimerkezleri",
            response_model=OnemliYerWrapper[SaglikKurumu],
        )

    async def get_agiz_dis_sagligi_merkezleri_list(
        self,
    ) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Ağız ve diş sağlığı merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/agizvedissagligimerkezleri
        """
        return await self._client.get(
            "ibb/cbs/agizvedissagligimerkezleri",
            response_model=OnemliYerWrapper[SaglikKurumu],
        )

    async def get_ana_cocuk_sagligi_merkezleri_list(
        self,
    ) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Ana çocuk sağlığı merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/anacocuksagligimerkezleri
        """
        return await self._client.get(
            "ibb/cbs/anacocuksagligimerkezleri",
            response_model=OnemliYerWrapper[SaglikKurumu],
        )

    async def get_dal_merkezleri_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Dal merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/dalmerkezleri
        """
        return await self._client.get(
            "ibb/cbs/dalmerkezleri", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_hastaneler_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Hastaneler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/hastaneler
        """
        return await self._client.get(
            "ibb/cbs/hastaneler", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_kan_merkezleri_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Kan merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kanmerkezleri
        """
        return await self._client.get(
            "ibb/cbs/kanmerkezleri", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_laboratuvarlar_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Laboratuvarlar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/laboratuvarlar
        """
        return await self._client.get(
            "ibb/cbs/laboratuvarlar", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_poliklinikler_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Poliklinikler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/poliklinikler
        """
        return await self._client.get(
            "ibb/cbs/poliklinikler", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_tip_merkezleri_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Tıp merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/tipmerkezleri
        """
        return await self._client.get(
            "ibb/cbs/tipmerkezleri", response_model=OnemliYerWrapper[SaglikKurumu]
        )

    async def get_toplum_sagligi_merkezleri_list(
        self,
    ) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Toplum sağlığı merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/toplumsakligimerkezleri
        """
        return await self._client.get(
            "ibb/cbs/toplumsagligimerkezleri",
            response_model=OnemliYerWrapper[SaglikKurumu],
        )

    async def get_verem_savas_dispanserleri_list(
        self,
    ) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Verem savaş dispanserleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/veremsavasdispanserleri
        """
        return await self._client.get(
            "ibb/cbs/veremsavasdispanserleri",
            response_model=OnemliYerWrapper[SaglikKurumu],
        )

    async def get_veterinerlikler_list(self) -> OnemliYerWrapper[SaglikKurumu]:
        """
        Veterinerlikler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/veterinerlikler
        """
        return await self._client.get(
            "ibb/cbs/veterinerlikler", response_model=OnemliYerWrapper[SaglikKurumu]
        )
