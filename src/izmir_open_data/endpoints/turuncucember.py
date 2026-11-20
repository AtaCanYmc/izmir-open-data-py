from typing import Any

from izmir_open_data.endpoints.base import BaseEndpoint


class TuruncuCemberEndpoint(BaseEndpoint):
    """Turuncu Cember hygiene certification endpoint."""

    async def get_isletmeler(self) -> list[dict[str, Any]]:
        """List active certified businesses."""
        return await self._client.get("ibb/turuncucember/isletmeler")

    async def get_isletme(self, isletme_id: int) -> dict[str, Any]:
        """Get certificate details of a specific business."""
        return await self._client.get(f"ibb/turuncucember/isletme/{isletme_id}")

    async def get_sayilar(self) -> dict[str, Any]:
        """Get application and certification statistics."""
        return await self._client.get("ibb/turuncucember/sayilar")
