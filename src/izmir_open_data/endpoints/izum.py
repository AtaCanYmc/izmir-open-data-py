from typing import Any

from izmir_open_data.endpoints.base import BaseEndpoint

IZUM_RESOURCES = {
    "HIZ_VE_SURE": "a3bd880f-dfc6-4f65-bbfd-5fcc998268c3",
    "VMS_PANOLAR": "c1bcea54-bdf6-417f-b807-6d695afed56f",
    "ARAC_SAYIM": "25866cc4-298a-4ee7-bfd3-719ea7f530b2",
}


class IzumEndpoint(BaseEndpoint):
    """Izmir Transportation Center (İZUM) endpoint."""

    async def get_ana_arter_hiz_ve_sure(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query main arterial roads daily speed and travel time data."""
        params: dict[str, Any] = {
            "resource_id": IZUM_RESOURCES["HIZ_VE_SURE"],
            "limit": limit,
            "offset": offset,
        }
        if q:
            params["q"] = q
        if filters:
            params["filters"] = filters
        if sort:
            params["sort"] = sort
        return await self._client.get_ckan("datastore_search", params=params)

    async def get_vms_panolari(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query Variable Message Signs (VMS) locations and dimensions."""
        params: dict[str, Any] = {
            "resource_id": IZUM_RESOURCES["VMS_PANOLAR"],
            "limit": limit,
            "offset": offset,
        }
        if q:
            params["q"] = q
        if filters:
            params["filters"] = filters
        if sort:
            params["sort"] = sort
        return await self._client.get_ckan("datastore_search", params=params)

    async def get_arac_sayim_verileri(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query arterial roads vehicle traffic count data."""
        params: dict[str, Any] = {
            "resource_id": IZUM_RESOURCES["ARAC_SAYIM"],
            "limit": limit,
            "offset": offset,
        }
        if q:
            params["q"] = q
        if filters:
            params["filters"] = filters
        if sort:
            params["sort"] = sort
        return await self._client.get_ckan("datastore_search", params=params)

    async def get_otoparklar(self) -> list[dict[str, Any]]:
        """Get İZUM live parking occupancy and location data."""
        return await self._client.get("ibb/izum/otoparklar")

    async def get_kameralar(self) -> list[dict[str, Any]]:
        """Get traffic monitoring camera list via CSV."""
        return await self._client.get_csv(
            "https://acikveri.bizizmir.com/dataset/a5cda2f2-ccbd-4fac-a4bb-c691abff28f1/resource/b91cb15d-05c6-45b7-8a75-48e030aad368/download/trafikkameralari.csv"
        )

    async def dump_ana_arter_hiz_ve_sure(self) -> Any:
        """Download complete speed and duration dump."""
        return await self._client.get_ckan_dump(IZUM_RESOURCES["HIZ_VE_SURE"])

    async def dump_arac_sayim_verileri(self) -> Any:
        """Download vehicle count dump."""
        return await self._client.get_ckan_dump(IZUM_RESOURCES["ARAC_SAYIM"])
