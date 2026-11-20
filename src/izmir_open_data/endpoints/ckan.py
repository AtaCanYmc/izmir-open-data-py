from typing import Any

from izmir_open_data.endpoints.base import BaseEndpoint
from izmir_open_data.endpoints.ckan_query_builder import CKANQueryBuilder


class CKANEndpoint(BaseEndpoint):
    """CKAN Open Data Portal endpoint (acikveri.bizizmir.com)."""

    def query(self, resource_id: str) -> CKANQueryBuilder:
        """Start a fluent query builder for the specified CKAN Datastore resource."""
        return CKANQueryBuilder(self._client, resource_id)

    async def search_packages(
        self,
        query: str | dict[str, Any] | None = None,
        rows: int = 10,
        start: int = 0,
        sort: str | None = None,
        fq: str | None = None,
        **extra_params: Any,
    ) -> dict[str, Any]:
        """Search across all datasets on the portal."""
        params: dict[str, Any] = {}
        if isinstance(query, str):
            params["q"] = query
        elif isinstance(query, dict):
            params.update(query)

        params.setdefault("rows", rows)
        params.setdefault("start", start)
        if sort:
            params["sort"] = sort
        if fq:
            params["fq"] = fq
        params.update(extra_params)

        return await self._client.get_ckan("package_search", params=params)

    async def get_package(self, id_or_name: str) -> dict[str, Any]:
        """Get dataset metadata and resources by ID or slug."""
        return await self._client.get_ckan("package_show", params={"id": id_or_name})

    async def list_packages(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[str]:
        """List all dataset slugs in the portal."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return await self._client.get_ckan("package_list", params=params)

    async def search_datastore(
        self,
        resource_id: str,
        q: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        offset: int = 0,
        sort: str | None = None,
        fields: list[str] | str | None = None,
    ) -> dict[str, Any]:
        """Query records from any active CKAN Datastore resource."""
        params: dict[str, Any] = {
            "resource_id": resource_id,
            "limit": limit,
            "offset": offset,
        }
        if q:
            params["q"] = q
        if filters:
            params["filters"] = filters
        if sort:
            params["sort"] = sort
        if fields:
            params["fields"] = ",".join(fields) if isinstance(fields, list) else fields

        return await self._client.get_ckan("datastore_search", params=params)

    async def dump_datastore(self, resource_id: str) -> Any:
        """Download complete dump of a datastore resource in JSON format."""
        return await self._client.get_ckan_dump(resource_id)

    async def list_organizations(self) -> list[str]:
        """List publisher organizations on the portal."""
        return await self._client.get_ckan("organization_list")

    async def list_groups(self) -> list[str]:
        """List category groups on the portal."""
        return await self._client.get_ckan("group_list")

    async def list_tags(self, query: str | None = None) -> list[str]:
        """List dataset tags on the portal."""
        params = {"query": query} if query else {}
        return await self._client.get_ckan("tag_list", params=params)
