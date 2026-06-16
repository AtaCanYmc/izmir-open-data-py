import httpx
from pydantic import BaseModel
from typing import Any, Dict, Optional


class IzmirClient:
    """Async client for Izmir Open Data API."""

    BASE_URL = "https://openapi.izmir.bel.tr/api"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        # Set a default user agent and basic headers
        headers["User-Agent"] = "izmir-open-data-py/0.1.0"
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, headers=headers)

    async def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Fetch a specific dataset by ID."""
        response = await self.client.get(f"/ibb/{dataset_id}")
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self) -> "IzmirClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
