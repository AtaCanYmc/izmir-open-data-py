from typing import Any

from izmir_open_data.endpoints.base import BaseEndpoint

TUVALET_RESOURCES = {
    "AKILLI_TUVALETLER": "d87de3c1-9bc0-4a8c-842a-90cd2a30d03a",
    "MODULER_TUVALETLER": "8f6e905d-3f76-45e5-b52a-b89be7d4631b",
}


class TuvaletEndpoint(BaseEndpoint):
    """Smart and Modular Public Toilets endpoint."""

    async def get_akilli_tuvaletler(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query smart public toilets location and facility data."""
        params: dict[str, Any] = {
            "resource_id": TUVALET_RESOURCES["AKILLI_TUVALETLER"],
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

    async def get_moduler_tuvaletler(
        self,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """Query modular toilets and baby care rooms with accessibility info."""
        params: dict[str, Any] = {
            "resource_id": TUVALET_RESOURCES["MODULER_TUVALETLER"],
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

    async def dump_akilli_tuvaletler(self) -> Any:
        """Download complete smart toilets data dump."""
        return await self._client.get_ckan_dump(TUVALET_RESOURCES["AKILLI_TUVALETLER"])

    async def dump_moduler_tuvaletler(self) -> Any:
        """Download complete modular toilets data dump."""
        return await self._client.get_ckan_dump(TUVALET_RESOURCES["MODULER_TUVALETLER"])
