from typing import Any

from izmir_open_data.endpoints.base import BaseEndpoint

ITFAIYE_RESOURCES = {
    "ACIL_MUDAHALE": "4b7a8da1-94ed-487f-8b7a-e13d40a5cd33",
    "EGITIM_HIZMETLERI": "db592f6e-4694-470f-be03-64444fc0bb88",
}


class ItfaiyeEndpoint(BaseEndpoint):
    """Fire Department (İtfaiye) endpoint."""

    async def get_gruplar(self) -> dict[str, Any] | list[dict[str, Any]]:
        """List fire stations and groups across Izmir (CBS)."""
        return await self._client.get("ibb/cbs/itfaiyegruplari")

    async def get_acil_mudahale_istatistigi(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query emergency fire/rescue incident statistics."""
        params: dict[str, Any] = {
            "resource_id": ITFAIYE_RESOURCES["ACIL_MUDAHALE"],
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

    async def get_egitim_hizmetleri(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query fire department training services statistics."""
        params: dict[str, Any] = {
            "resource_id": ITFAIYE_RESOURCES["EGITIM_HIZMETLERI"],
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

    async def dump_acil_mudahale(self) -> Any:
        """Download emergency incident statistics dump."""
        return await self._client.get_ckan_dump(ITFAIYE_RESOURCES["ACIL_MUDAHALE"])

    async def dump_egitim_hizmetleri(self) -> Any:
        """Download training services statistics dump."""
        return await self._client.get_ckan_dump(ITFAIYE_RESOURCES["EGITIM_HIZMETLERI"])
