from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from izmir_open_data.core.client import IzmirClient


class BaseEndpoint:
    """Base class for all Izmir Open Data API endpoint groups."""

    def __init__(self, client: "IzmirClient"):
        self._client = client
