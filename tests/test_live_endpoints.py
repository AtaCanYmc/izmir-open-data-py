import inspect
from datetime import date

import pytest
from izmir_open_data.core.client import IzmirClient
from izmir_open_data.endpoints.base import BaseEndpoint


def get_all_endpoints() -> list[tuple[str, str]]:
    client = IzmirClient()
    endpoints = []
    for attr_name in dir(client):
        if attr_name.startswith("_"):
            continue
        group = getattr(client, attr_name)
        if isinstance(group, BaseEndpoint):
            for method_name in dir(group):
                if method_name.startswith("get_"):
                    endpoints.append((attr_name, method_name))
    return endpoints


@pytest.mark.asyncio
@pytest.mark.parametrize("group_name, method_name", get_all_endpoints())
async def test_endpoint_live(group_name: str, method_name: str) -> None:
    """
    Tüm endpoint'leri otomatik olarak keşfeder ve canlı API'ye istek atar.
    Amacımız her bir endpoint'in şu an 200 OK dönüp dönmediğini (aktifliğini) test etmektir.
    """
    async with IzmirClient() as client:
        group = getattr(client, group_name)
        method = getattr(group, method_name)

        sig = inspect.signature(method)
        from typing import Any

        kwargs: dict[str, Any] = {}
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            if param.default != inspect.Parameter.empty:
                continue

            # Zorunlu parametreler için dummy (örnek) veriler oluşturuyoruz
            if param.annotation is int:
                kwargs[param_name] = 1
            elif param.annotation is str:
                kwargs[param_name] = "1"
            elif param.annotation is date:
                kwargs[param_name] = date(2023, 1, 1)  # Geçmiş bir tarih
            elif param.annotation is float:
                kwargs[param_name] = 1.0
            else:
                kwargs[param_name] = 1  # Fallback

        try:
            # Endpoint'e istek at
            await method(**kwargs)
        except Exception as e:
            # Hata fırlatılırsa testi başarısız say ve hatayı yazdır
            pytest.fail(f"Endpoint {group_name}.{method_name} failed: {e}")
