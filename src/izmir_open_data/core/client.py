import csv
import io
import re
import urllib.parse
from typing import Any

import httpx

from izmir_open_data.core.cache import CacheProvider, MemoryCache
from izmir_open_data.core.exceptions import APIError
from izmir_open_data.core.retry import RetryConfig, execute_with_retry
from izmir_open_data.endpoints.afetler import AfetlerEndpoint
from izmir_open_data.endpoints.bisim import BisimEndpoint
from izmir_open_data.endpoints.ckan import CKANEndpoint
from izmir_open_data.endpoints.cografi import CografiEndpoint
from izmir_open_data.endpoints.eczaneler import EczanelerEndpoint
from izmir_open_data.endpoints.egitim import EgitimEndpoint
from izmir_open_data.endpoints.eshot import EshotEndpoint
from izmir_open_data.endpoints.etkinlikler import EtkinliklerEndpoint
from izmir_open_data.endpoints.hizmet import HizmetEndpoint
from izmir_open_data.endpoints.iklim import IklimEndpoint
from izmir_open_data.endpoints.itfaiye import ItfaiyeEndpoint
from izmir_open_data.endpoints.izban import IzbanEndpoint
from izmir_open_data.endpoints.izmirimkart import IzmirimKartEndpoint
from izmir_open_data.endpoints.izsu import IzsuEndpoint
from izmir_open_data.endpoints.iztek import IztekEndpoint
from izmir_open_data.endpoints.izum import IzumEndpoint
from izmir_open_data.endpoints.kamu import KamuEndpoint
from izmir_open_data.endpoints.kutuphane import KutuphaneEndpoint
from izmir_open_data.endpoints.metro import MetroEndpoint
from izmir_open_data.endpoints.muhtarliklar import MuhtarliklarEndpoint
from izmir_open_data.endpoints.otopark import OtoparkEndpoint
from izmir_open_data.endpoints.pazarlar import PazarlarEndpoint
from izmir_open_data.endpoints.plaj import PlajEndpoint
from izmir_open_data.endpoints.saglik import SaglikEndpoint
from izmir_open_data.endpoints.sosyal import SosyalEndpoint
from izmir_open_data.endpoints.spor import SporEndpoint
from izmir_open_data.endpoints.taksi import TaksiEndpoint
from izmir_open_data.endpoints.tarihi import TarihiEndpoint
from izmir_open_data.endpoints.trafik import TrafikEndpoint
from izmir_open_data.endpoints.tramvay import TramvayEndpoint
from izmir_open_data.endpoints.tren import TrenEndpoint
from izmir_open_data.endpoints.turuncucember import TuruncuCemberEndpoint
from izmir_open_data.endpoints.tuvalet import TuvaletEndpoint
from izmir_open_data.endpoints.vapur import VapurEndpoint
from izmir_open_data.endpoints.wizmirnet import WizmirnetEndpoint


class IzmirClient:
    """Async client for Izmir Open Data API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://openapi.izmir.bel.tr/api/",
        ckan_base_url: str = "https://acikveri.bizizmir.com/api/3/action/",
        ckan_dump_base_url: str = "https://acikveri.bizizmir.com/datastore/dump/",
        cache: bool | CacheProvider | None = None,
        retry: bool | RetryConfig | None = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.ckan_base_url = ckan_base_url
        self.ckan_dump_base_url = ckan_dump_base_url
        self.retry_config = retry

        if cache is True:
            self._cache: CacheProvider | None = MemoryCache()
        elif cache:
            self._cache = cache
        else:
            self._cache = None

        headers = {"User-Agent": "izmir-open-data-py/0.3.1"}  # x-release-please-version
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self._client = httpx.AsyncClient(headers=headers, timeout=timeout)
        self._init_endpoints()

    @property
    def cache(self) -> CacheProvider | None:
        """Active cache provider."""
        return self._cache

    async def clear_cache(self) -> None:
        """Clear all entries in the cache."""
        if self._cache:
            await self._cache.clear()

    def _init_endpoints(self) -> None:
        """Initialize all endpoint namespaces."""
        self.afetler = AfetlerEndpoint(self)
        self.bisim = BisimEndpoint(self)
        self.cografi = CografiEndpoint(self)
        self.eczaneler = EczanelerEndpoint(self)
        self.egitim = EgitimEndpoint(self)
        self.eshot = EshotEndpoint(self)
        self.etkinlikler = EtkinliklerEndpoint(self)
        self.hizmet = HizmetEndpoint(self)
        self.iklim = IklimEndpoint(self)
        self.izban = IzbanEndpoint(self)
        self.izmirimkart = IzmirimKartEndpoint(self)
        self.izsu = IzsuEndpoint(self)
        self.iztek = IztekEndpoint(self)
        self.kamu = KamuEndpoint(self)
        self.kutuphane = KutuphaneEndpoint(self)
        self.metro = MetroEndpoint(self)
        self.muhtarliklar = MuhtarliklarEndpoint(self)
        self.otopark = OtoparkEndpoint(self)
        self.pazarlar = PazarlarEndpoint(self)
        self.plaj = PlajEndpoint(self)
        self.saglik = SaglikEndpoint(self)
        self.sosyal = SosyalEndpoint(self)
        self.spor = SporEndpoint(self)
        self.taksi = TaksiEndpoint(self)
        self.tarihi = TarihiEndpoint(self)
        self.trafik = TrafikEndpoint(self)
        self.tramvay = TramvayEndpoint(self)
        self.tren = TrenEndpoint(self)
        self.vapur = VapurEndpoint(self)
        self.wizmirnet = WizmirnetEndpoint(self)

        # New CKAN and portal modules
        self.ckan = CKANEndpoint(self)
        self.itfaiye = ItfaiyeEndpoint(self)
        self.izum = IzumEndpoint(self)
        self.turuncucember = TuruncuCemberEndpoint(self)
        self.tuvalet = TuvaletEndpoint(self)

    async def get(self, path: str, response_model: Any = None) -> Any:
        """Standard API fetch with cache, retry, and path traversal protection."""
        normalized_path = path.lstrip("/")
        unquoted = urllib.parse.unquote(normalized_path)
        if (
            ".." in unquoted
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", unquoted)
            or unquoted.startswith("//")
        ):
            raise ValueError(f"Geçersiz veya güvensiz istek yolu: {path}")

        url = f"{self.base_url.rstrip('/')}/{normalized_path}"
        cache_key = f"GET:{url}"

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return cached

        async def _fetch():
            response = await self._client.get(url)
            if not response.is_success:
                raise APIError(
                    f"API response error: {response.status_code}", response.status_code
                )
            if response.status_code == 204:
                return None
            data = response.json()
            if response_model:
                from pydantic import TypeAdapter

                return TypeAdapter(response_model).validate_python(data)
            return data

        result = (
            await execute_with_retry(_fetch, self.retry_config)
            if self.retry_config
            else await _fetch()
        )

        if self._cache and result is not None:
            await self._cache.set(cache_key, result)

        return result

    async def get_ckan(
        self,
        action: str,
        params: dict[str, Any] | None = None,
        response_model: Any = None,
    ) -> Any:
        """Fetch from CKAN API with cache, retry, and safety protections."""
        clean_action = action.lstrip("/")
        unquoted_action = urllib.parse.unquote(clean_action)
        if (
            ".." in unquoted_action
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", unquoted_action)
            or unquoted_action.startswith("//")
        ):
            raise ValueError(f"Geçersiz veya güvensiz CKAN aksiyonu: {action}")

        url = f"{self.ckan_base_url.rstrip('/')}/{clean_action}"
        query_params = params or {}

        # Prepare cache key including sorted query params
        encoded_qs = urllib.parse.urlencode(
            sorted(
                [
                    (
                        k,
                        v
                        if not isinstance(v, (dict, list))
                        else httpx.Response(200, json=v).text,
                    )
                    for k, v in query_params.items()
                ]
            )
        )
        cache_key = f"CKAN:{url}?{encoded_qs}" if encoded_qs else f"CKAN:{url}"

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return cached

        async def _fetch():
            # For complex objects in params, convert to string
            formatted_params = {}
            for k, v in query_params.items():
                if v is not None:
                    if isinstance(v, (dict, list)):
                        import json

                        formatted_params[k] = json.dumps(v)
                    else:
                        formatted_params[k] = v

            response = await self._client.get(url, params=formatted_params)
            if not response.is_success:
                raise APIError(
                    f"CKAN API response error: {response.status_code}",
                    response.status_code,
                )

            data = response.json()
            if data.get("success"):
                res = data.get("result")
                if response_model:
                    from pydantic import TypeAdapter

                    return TypeAdapter(response_model).validate_python(res)
                return res
            else:
                error_msg = data.get("error", {}).get("message", "Unknown CKAN error")
                raise APIError(f"CKAN Error: {error_msg}")

        result = (
            await execute_with_retry(_fetch, self.retry_config)
            if self.retry_config
            else await _fetch()
        )

        if self._cache and result is not None:
            await self._cache.set(cache_key, result)

        return result

    async def get_ckan_dump(self, resource_id: str, response_model: Any = None) -> Any:
        """Fetch from CKAN Dump API with URL encoding."""
        clean_id = urllib.parse.quote(resource_id.strip(), safe="")
        url = f"{self.ckan_dump_base_url.rstrip('/')}/{clean_id}?format=json"
        cache_key = f"DUMP:{url}"

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return cached

        async def _fetch():
            response = await self._client.get(url, timeout=30.0)
            if not response.is_success:
                raise APIError(
                    f"CKAN Dump API response error: {response.status_code}",
                    response.status_code,
                )

            data = response.json()
            if response_model:
                from pydantic import TypeAdapter

                return TypeAdapter(response_model).validate_python(data)
            return data

        result = (
            await execute_with_retry(_fetch, self.retry_config)
            if self.retry_config
            else await _fetch()
        )

        if self._cache and result is not None:
            await self._cache.set(cache_key, result)

        return result

    async def get_csv(self, url: str, delimiter: str = ";") -> list[dict[str, Any]]:
        """Fetch and parse CSV data with prototype/pollution protection."""
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                "CSV istekleri yalnızca HTTP veya HTTPS şemalarını destekler."
            )

        cache_key = f"CSV:{url}"

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return cached

        async def _fetch():
            response = await self._client.get(url, timeout=30.0)
            if not response.is_success:
                raise APIError(
                    f"CSV API response error: {response.status_code}",
                    response.status_code,
                )

            text = response.text
            f = io.StringIO(text.strip())
            reader = csv.DictReader(f, delimiter=delimiter)

            results = []
            disallowed_fields = {"__proto__", "constructor", "prototype"}

            if reader.fieldnames:
                cleaned_fieldnames = [f.strip().strip('"') for f in reader.fieldnames]
                reader.fieldnames = cleaned_fieldnames

                for row in reader:
                    cleaned_row = {}
                    for k, v in row.items():
                        if k is None or k in disallowed_fields:
                            continue
                        val = v.strip().strip('"') if v else ""
                        if (
                            val == ""
                            or ":" in val
                            or "-" in val
                            or val.lower() in ("true", "false")
                        ):
                            cleaned_row[k] = val
                        else:
                            try:
                                if "." in val:
                                    cleaned_row[k] = float(val)
                                else:
                                    cleaned_row[k] = int(val)
                            except ValueError:
                                cleaned_row[k] = val
                    results.append(cleaned_row)

            return results

        result = (
            await execute_with_retry(_fetch, self.retry_config)
            if self.retry_config
            else await _fetch()
        )

        if self._cache and result is not None:
            await self._cache.set(cache_key, result)

        return result

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "IzmirClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
