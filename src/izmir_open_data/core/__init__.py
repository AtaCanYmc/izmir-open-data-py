"""Core client, caching, retry, streaming, and data format utilities."""

from izmir_open_data.core.cache import CacheProvider, MemoryCache
from izmir_open_data.core.client import IzmirClient
from izmir_open_data.core.dataframes import normalize_records, to_dataframe, to_polars
from izmir_open_data.core.exceptions import APIError
from izmir_open_data.core.geojson import extract_coordinates, to_geojson
from izmir_open_data.core.parquet import read_parquet, to_geoparquet, to_parquet
from izmir_open_data.core.retry import RetryConfig
from izmir_open_data.core.stream import stream, stream_batches

__all__ = [
    "APIError",
    "CacheProvider",
    "IzmirClient",
    "MemoryCache",
    "RetryConfig",
    "extract_coordinates",
    "normalize_records",
    "read_parquet",
    "stream",
    "stream_batches",
    "to_dataframe",
    "to_geojson",
    "to_geoparquet",
    "to_parquet",
    "to_polars",
]
