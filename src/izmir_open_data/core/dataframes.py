from typing import Any


def normalize_records(data: Any) -> list[dict[str, Any]]:
    """Extract and normalize records from API responses, wrappers, or models."""
    if data is None:
        return []

    items: list[Any] = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get("records"), list):
            items = data["records"]
        elif isinstance(data.get("kayitlar"), list):
            items = data["kayitlar"]
        elif isinstance(data.get("onemliyer"), list):
            items = data["onemliyer"]
        elif isinstance(data.get("results"), list):
            items = data["results"]
        else:
            items = [data]
    elif hasattr(data, "kayitlar") and isinstance(data.kayitlar, list):
        items = data.kayitlar
    elif hasattr(data, "model_dump"):
        dumped = data.model_dump()
        if isinstance(dumped, dict):
            if isinstance(dumped.get("kayitlar"), list):
                items = dumped["kayitlar"]
            elif isinstance(dumped.get("records"), list):
                items = dumped["records"]
            elif isinstance(dumped.get("onemliyer"), list):
                items = dumped["onemliyer"]
            else:
                items = [dumped]
        else:
            items = [dumped]
    else:
        items = [data]

    normalized: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            normalized.append(dict(item))
        elif hasattr(item, "model_dump"):
            normalized.append(item.model_dump())
        elif hasattr(item, "__dict__"):
            normalized.append(
                {k: v for k, v in item.__dict__.items() if not k.startswith("_")}
            )
        else:
            normalized.append({"value": item})

    return normalized


def to_dataframe(data: Any) -> Any:
    """Convert API response data directly to a Pandas DataFrame."""
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            "Pandas kütüphanesi yüklü değil. 'pip install pandas' veya "
            "'pip install izmir-open-data-py[data]' ile yükleyebilirsiniz."
        ) from e

    records = normalize_records(data)
    return pd.DataFrame(records)


def to_polars(data: Any) -> Any:
    """Convert API response data directly to a Polars DataFrame."""
    try:
        import polars as pl
    except ImportError as e:
        raise ImportError(
            "Polars kütüphanesi yüklü değil. 'pip install polars' veya "
            "'pip install izmir-open-data-py[data]' ile yükleyebilirsiniz."
        ) from e

    records = normalize_records(data)
    if not records:
        return pl.DataFrame()
    return pl.from_dicts(records)
