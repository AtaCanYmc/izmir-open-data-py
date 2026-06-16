import csv
import io
from typing import Any

import httpx
from izmir_open_data.core.exceptions import APIError
from izmir_open_data.endpoints.afetler import AfetlerEndpoint
from izmir_open_data.endpoints.bisim import BisimEndpoint
from izmir_open_data.endpoints.cografi import CografiEndpoint
from izmir_open_data.endpoints.eczaneler import EczanelerEndpoint
from izmir_open_data.endpoints.egitim import EgitimEndpoint
from izmir_open_data.endpoints.eshot import EshotEndpoint
from izmir_open_data.endpoints.etkinlikler import EtkinliklerEndpoint
from izmir_open_data.endpoints.hizmet import HizmetEndpoint
from izmir_open_data.endpoints.iklim import IklimEndpoint
from izmir_open_data.endpoints.izban import IzbanEndpoint
from izmir_open_data.endpoints.izmirimkart import IzmirimKartEndpoint
from izmir_open_data.endpoints.izsu import IzsuEndpoint
from izmir_open_data.endpoints.iztek import IztekEndpoint
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
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.ckan_base_url = ckan_base_url
        self.ckan_dump_base_url = ckan_dump_base_url

        headers = {"User-Agent": "izmir-open-data-py/0.1.0"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # We don't set base_url here because we request from multiple different base URLs
        self._client = httpx.AsyncClient(headers=headers, timeout=30.0)

        # Endpoints will be attached dynamically or initialized later
        self._init_endpoints()

    def _init_endpoints(self):
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

    async def get(self, path: str, response_model: Any = None) -> Any:
        """Standard API fetch."""
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        response = await self._client.get(url)
        if not response.is_success:
            raise APIError(
                f"API response error: {response.status_code}", response.status_code
            )

        # Eğer 204 No Content dönerse, JSON parse etmeye çalışmadan None döndür.
        if response.status_code == 204:
            return None

        data = response.json()
        if response_model:
            from pydantic import TypeAdapter

            return TypeAdapter(response_model).validate_python(data)
        return data

    async def get_ckan(
        self,
        action: str,
        params: dict[str, Any] | None = None,
        response_model: Any = None,
    ) -> Any:
        """Fetch from CKAN API."""
        url = f"{self.ckan_base_url.rstrip('/')}/{action.lstrip('/')}"
        response = await self._client.get(url, params=params or {})
        if not response.is_success:
            raise APIError(
                f"CKAN API response error: {response.status_code}", response.status_code
            )

        data = response.json()
        if data.get("success"):
            result = data.get("result")
            if response_model:
                from pydantic import TypeAdapter

                return TypeAdapter(response_model).validate_python(result)
            return result
        else:
            error_msg = data.get("error", {}).get("message", "Unknown CKAN error")
            raise APIError(f"CKAN Error: {error_msg}")

    async def get_ckan_dump(self, resource_id: str, response_model: Any = None) -> Any:
        """Fetch from CKAN Dump API."""
        url = f"{self.ckan_dump_base_url.rstrip('/')}/{resource_id.lstrip('/')}?format=json"
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

    async def get_csv(self, url: str, delimiter: str = ";") -> list[dict[str, Any]]:
        """Fetch and parse CSV data."""
        response = await self._client.get(url, timeout=30.0)
        if not response.is_success:
            raise APIError(
                f"CSV API response error: {response.status_code}", response.status_code
            )

        text = response.text
        # Use csv module to parse
        f = io.StringIO(text.strip())
        reader = csv.DictReader(f, delimiter=delimiter)

        results = []
        if reader.fieldnames:
            # Clean field names by stripping whitespace and quotes
            cleaned_fieldnames = [f.strip().strip('"') for f in reader.fieldnames]
            reader.fieldnames = cleaned_fieldnames

            for row in reader:
                cleaned_row = {}
                for k, v in row.items():
                    if k is None:
                        continue
                    val = v.strip().strip('"') if v else ""
                    # Convert to number if possible, but keep string if it contains special chars like : or -
                    if (
                        val == ""
                        or ":" in val
                        or "-" in val
                        or val.lower() in ("true", "false")
                    ):
                        cleaned_row[k] = val
                    else:
                        try:
                            # Try integer first
                            if "." in val:
                                cleaned_row[k] = float(val)
                            else:
                                cleaned_row[k] = int(val)
                        except ValueError:
                            cleaned_row[k] = val
                results.append(cleaned_row)

        return results

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "IzmirClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
