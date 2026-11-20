"""Izmir Open Data Python Client."""

__version__ = "0.3.0"  # x-release-please-version

from .core.cache import CacheProvider, MemoryCache
from .core.client import IzmirClient
from .core.dataframes import normalize_records, to_dataframe, to_polars
from .core.geojson import extract_coordinates, to_geojson, to_geojson_feature
from .core.parquet import read_parquet, to_geoparquet, to_parquet
from .core.retry import RetryConfig, execute_with_retry
from .core.stream import stream_batches, stream_records
from .endpoints.ckan_query_builder import CKANQueryBuilder
from .testing import MockIzmirClient, get_fixture

# Alias IzmirAPI to IzmirClient for parity with izmir-open-data-js
IzmirAPI = IzmirClient

__all__ = [
    "IzmirClient",
    "IzmirAPI",
    "MemoryCache",
    "CacheProvider",
    "RetryConfig",
    "execute_with_retry",
    "extract_coordinates",
    "to_geojson_feature",
    "to_geojson",
    "CKANQueryBuilder",
    "to_dataframe",
    "to_polars",
    "normalize_records",
    "to_parquet",
    "read_parquet",
    "to_geoparquet",
    "stream_records",
    "stream_batches",
    "MockIzmirClient",
    "get_fixture",
]
