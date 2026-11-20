"""Izmir Open Data Python Client."""

__version__ = "0.2.0"

from .core.cache import CacheProvider, MemoryCache
from .core.client import IzmirClient
from .core.geojson import extract_coordinates, to_geojson, to_geojson_feature
from .core.retry import RetryConfig, execute_with_retry
from .endpoints.ckan_query_builder import CKANQueryBuilder

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
]
