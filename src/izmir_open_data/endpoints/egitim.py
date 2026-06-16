from izmir_open_data.core.types import DefaultOnemliYer, OnemliYerWrapper
from izmir_open_data.endpoints.base import BaseEndpoint


class EgitimKurumu(DefaultOnemliYer):
    pass

class EgitimEndpoint(BaseEndpoint):
    async def get_engelli_okullari_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Engelliler okulu konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/engelliokullari
        """
        return await self._client.get("ibb/cbs/engelliokullari")

    async def get_anaokullar_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Anaokulu konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/anaokullari
        """
        return await self._client.get("ibb/cbs/anaokullari")

    async def get_etut_merkezleri_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Etüt eğitim merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/etutmerkezleri
        """
        return await self._client.get("ibb/cbs/etutmerkezleri")

    async def get_halk_egitim_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Halk eğitim merkezleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/halkegitim
        """
        return await self._client.get("ibb/cbs/halkegitim")

    async def get_ilkokullar_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        İlkokullar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ilkokullar
        """
        return await self._client.get("ibb/cbs/ilkokullar")

    async def get_kolejler_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Kolejler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/kolejler
        """
        return await self._client.get("ibb/cbs/kolejler")

    async def get_liseler_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Liseler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/liseler
        """
        return await self._client.get("ibb/cbs/liseler")

    async def get_meslek_liseleri_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Meslek liseleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/meslekliseleri
        """
        return await self._client.get("ibb/cbs/meslekliseleri")

    async def get_ortaokullar_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Ortaokullar konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/ortaokullar
        """
        return await self._client.get("ibb/cbs/ortaokullar")

    async def get_sanat_okullari_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Sanat okulları konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/sanatokullari
        """
        return await self._client.get("ibb/cbs/sanatokullari")

    async def get_universiteler_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Üniversiteler konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/universiteler
        """
        return await self._client.get("ibb/cbs/universiteler")

    async def get_milli_egitim_list(self) -> OnemliYerWrapper[EgitimKurumu]:
        """
        Milli eğitim müdürlükleri konum bilgilerini içeren web servisi.
        Kaynak: https://openapi.izmir.bel.tr/api/ibb/cbs/milliegitim
        """
        return await self._client.get("ibb/cbs/milliegitim")
