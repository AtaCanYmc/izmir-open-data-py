import math
import re
from collections.abc import AsyncIterator
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from izmir_open_data.core.client import IzmirClient


class CKANQueryBuilder:
    """Fluent query builder for CKAN datastore."""

    def __init__(self, client: "IzmirClient", resource_id: str):
        self._client = client
        self.resource_id = resource_id
        self.search_filter: str | None = None
        self.field_filters: dict[str, Any] = {}
        self.record_limit: int = 100
        self.record_offset: int = 0
        self.sort_order: str | None = None
        self.selected_fields: list[str] | None = None

    def where(self, field: str, value: Any) -> "CKANQueryBuilder":
        self.field_filters[field] = value
        return self

    def filter(self, field: str, value: Any) -> "CKANQueryBuilder":
        return self.where(field, value)

    def where_all(self, filters: dict[str, Any]) -> "CKANQueryBuilder":
        self.field_filters.update(filters)
        return self

    def search(self, query: str) -> "CKANQueryBuilder":
        self.search_filter = query
        return self

    def limit(self, count: int) -> "CKANQueryBuilder":
        self.record_limit = count
        return self

    def offset(self, start_index: int) -> "CKANQueryBuilder":
        self.record_offset = start_index
        return self

    def page(self, page_number: int, page_size: int = 50) -> "CKANQueryBuilder":
        p = max(1, page_number)
        self.record_limit = page_size
        self.record_offset = (p - 1) * page_size
        return self

    def sort(self, field: str, direction: str = "asc") -> "CKANQueryBuilder":
        clean_dir = direction.lower().strip()
        if clean_dir not in ("asc", "desc"):
            clean_dir = "asc"
        clean_field = field.strip()
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", clean_field):
            raise ValueError(f"Geçersiz alan adı formatı: {field}")
        self.sort_order = f"{clean_field} {clean_dir}"
        return self

    def fields(self, fields_list: list[str]) -> "CKANQueryBuilder":
        self.selected_fields = fields_list
        return self

    def to_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "resource_id": self.resource_id,
            "limit": self.record_limit,
            "offset": self.record_offset,
        }
        if self.search_filter:
            params["q"] = self.search_filter
        if self.field_filters:
            params["filters"] = self.field_filters
        if self.sort_order:
            params["sort"] = self.sort_order
        if self.selected_fields:
            params["fields"] = self.selected_fields
        return params

    async def execute(self) -> dict[str, Any]:
        params = self.to_params()
        api_params = dict(params)
        if isinstance(api_params.get("fields"), list):
            api_params["fields"] = ",".join(api_params["fields"])
        return await self._client.get_ckan("datastore_search", params=api_params)

    async def fetch_all(
        self,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
    ) -> list[dict[str, Any]]:
        all_records: list[dict[str, Any]] = []
        async for batch in self.stream_batches(
            batch_size=batch_size, max_records=max_records
        ):
            all_records.extend(batch)
        return all_records

    async def stream_batches(
        self,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
    ) -> AsyncIterator[list[dict[str, Any]]]:
        """Stream matching records batch by batch."""
        current_offset = self.record_offset
        total_retrieved = 0

        while total_retrieved < max_records:
            current_limit = int(min(batch_size, max_records - total_retrieved))
            clone = CKANQueryBuilder(self._client, self.resource_id)
            clone.field_filters = dict(self.field_filters)
            clone.search_filter = self.search_filter
            clone.sort_order = self.sort_order
            clone.selected_fields = (
                list(self.selected_fields) if self.selected_fields else None
            )
            clone.record_limit = current_limit
            clone.record_offset = current_offset

            res = await clone.execute()
            records = res.get("records", []) if isinstance(res, dict) else []
            if not records:
                break

            yield records
            total_retrieved += len(records)
            current_offset += len(records)
            total = res.get("total", 0) if isinstance(res, dict) else 0

            if len(records) < current_limit or current_offset >= total:
                break

    async def stream(
        self,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream matching records item by item asynchronously."""
        async for batch in self.stream_batches(
            batch_size=batch_size, max_records=max_records
        ):
            for record in batch:
                yield record

    async def to_dataframe(
        self,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
    ) -> Any:
        """Fetch all records matching the query and return as a Pandas DataFrame."""
        from izmir_open_data.core.dataframes import to_dataframe

        records = await self.fetch_all(batch_size=batch_size, max_records=max_records)
        return to_dataframe(records)

    async def to_polars(
        self,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
    ) -> Any:
        """Fetch all records matching the query and return as a Polars DataFrame."""
        from izmir_open_data.core.dataframes import to_polars

        records = await self.fetch_all(batch_size=batch_size, max_records=max_records)
        return to_polars(records)

    async def to_parquet(
        self,
        path: str | Path,
        batch_size: int = 1000,
        max_records: int | float = math.inf,
        compression: str = "snappy",
    ) -> None:
        """Fetch matching records and store as a Parquet file."""
        from izmir_open_data.core.parquet import to_parquet

        records = await self.fetch_all(batch_size=batch_size, max_records=max_records)
        to_parquet(records, path=path, compression=compression)

    async def to_geoparquet(
        self,
        path: str | Path,
        geometry_column: str = "geometry",
        batch_size: int = 1000,
        max_records: int | float = math.inf,
        compression: str = "snappy",
    ) -> None:
        """Fetch matching records and store as a GeoParquet (v1.1.0) file."""
        from izmir_open_data.core.parquet import to_geoparquet

        records = await self.fetch_all(batch_size=batch_size, max_records=max_records)
        to_geoparquet(
            records,
            path=path,
            geometry_column=geometry_column,
            compression=compression,
        )
