from src.izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from src.izmir_open_data.endpoints.base import BaseEndpoint


class KamuKurumu(DefaultOnemliYer):
    pass

class KamuEndpoint(BaseEndpoint):
    async def get_bankalar_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Bankalar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/bankalar
        """
        response = await self._client.get("ibb/cbs/bankalar")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_belediyeler_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Belediye ve birimler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/belediyeler
        """
        response = await self._client.get("ibb/cbs/belediyeler")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_bolge_mudurlukleri_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Bölge müdürlükleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/bolgemudurlukleri
        """
        response = await self._client.get("ibb/cbs/bolgemudurlukleri")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_defterdarliklar_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Defterdarlık konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/defterdarliklar
        """
        response = await self._client.get("ibb/cbs/defterdarliklar")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_dernekler_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Dernekler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/dernekler
        """
        response = await self._client.get("ibb/cbs/dernekler")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_evlendirme_daireleri_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Evlendirme daireleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/evlendirmedaireleri
        """
        response = await self._client.get("ibb/cbs/evlendirmedaireleri")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_il_ilce_mudurlukleri_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        İl ve ilçe müdürlükleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ilveilcemudurlukleri
        """
        response = await self._client.get("ibb/cbs/ilveilcemudurlukleri")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_itfaiye_gruplari_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        İtfaiye grupları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/itfaiyegruplari
        """
        response = await self._client.get("ibb/cbs/itfaiyegruplari")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_konsolosluklar_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Konsolosluklar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/konsolosluklar
        """
        response = await self._client.get("ibb/cbs/konsolosluklar")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_meslek_odalari_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Meslek odaları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/meslekodalari
        """
        response = await self._client.get("ibb/cbs/meslekodalari")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_noterler_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Noterler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/noterler
        """
        response = await self._client.get("ibb/cbs/noterler")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_nufus_mudurlukleri_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Nüfus müdürlükleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/nufusmudurlukleri
        """
        response = await self._client.get("ibb/cbs/nufusmudurlukleri")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_ptt_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        PTT (Posta ve Telgraf Teşkilatı) konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ptt
        """
        response = await self._client.get("ibb/cbs/ptt")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_turizm_danisma_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Turizm danışma müdürlükleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/turizmdanisma
        """
        response = await self._client.get("ibb/cbs/turizmdanisma")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_vergi_daireleri_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Vergi daireleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/vergidaireleri
        """
        response = await self._client.get("ibb/cbs/vergidaireleri")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)

    async def get_maskematik_noktalari_list(self) -> OnemliYerWrapper[KamuKurumu]:
        """
        Maskematik istasyon noktaları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/maskematiknoktalari
        """
        response = await self._client.get("ibb/cbs/maskematiknoktalari")
        return OnemliYerWrapper[KamuKurumu].model_validate(response)
