from typing import Any

from izmir_open_data.core.client import IzmirClient
from izmir_open_data.testing.fixtures import FIXTURES


class MockIzmirClient(IzmirClient):
    """Offline test client that serves local fixtures without sending network requests."""

    def __init__(
        self,
        custom_fixtures: dict[str, Any] | None = None,
        simulate_error: Exception | None = None,
    ):
        super().__init__()
        self.fixtures = dict(FIXTURES)
        if custom_fixtures:
            self.fixtures.update(custom_fixtures)
        self.simulate_error = simulate_error
        self.recorded_calls: list[dict[str, Any]] = []

    async def get(self, path: str, response_model: Any = None) -> Any:
        self.recorded_calls.append({"type": "get", "path": path})
        if self.simulate_error:
            raise self.simulate_error

        clean_path = path.lower()
        if "eczane" in clean_path:
            data = self.fixtures["eczaneler"]
        elif "bisim" in clean_path:
            data = self.fixtures["bisim"]
        elif "otopark" in clean_path:
            data = self.fixtures["otoparklar"]
        elif "meydan" in clean_path:
            data = self.fixtures["cbs_meydanlar"]
        else:
            data = self.fixtures.get(clean_path, [])

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
        self.recorded_calls.append({"type": "ckan", "action": action, "params": params})
        if self.simulate_error:
            raise self.simulate_error

        res_id = (params or {}).get("resource_id", "")
        if "d87de3c1" in res_id:
            data = self.fixtures["tuvaletler"]
        elif "4b7a8da1" in res_id:
            data = self.fixtures["itfaiye"]
        elif "a3bd880f" in res_id:
            data = self.fixtures["izum"]
        else:
            data = {
                "include_total": True,
                "resource_id": res_id,
                "total": 1,
                "records": [{"_id": 1, "test": "mock_record"}],
            }

        if response_model:
            from pydantic import TypeAdapter

            return TypeAdapter(response_model).validate_python(data)
        return data

    async def get_ckan_dump(self, resource_id: str, response_model: Any = None) -> Any:
        self.recorded_calls.append({"type": "dump", "resource_id": resource_id})
        if self.simulate_error:
            raise self.simulate_error

        if "d87de3c1" in resource_id:
            data = self.fixtures["tuvaletler"]["records"]
        else:
            data = [{"_id": 1, "dump": "mock_dump"}]

        if response_model:
            from pydantic import TypeAdapter

            return TypeAdapter(response_model).validate_python(data)
        return data

    async def get_csv(self, url: str, delimiter: str = ";") -> list[dict[str, Any]]:
        self.recorded_calls.append({"type": "csv", "url": url})
        if self.simulate_error:
            raise self.simulate_error

        if "eshot" in url.lower() or "hat" in url.lower():
            return list(self.fixtures["eshot_hatlar"])
        return [{"col1": "val1", "col2": "val2"}]

    async def close(self) -> None:
        pass
