import json
import struct
from pathlib import Path
from typing import Any

from izmir_open_data.core.dataframes import normalize_records
from izmir_open_data.core.geojson import extract_coordinates


def _point_to_wkb(lon: float, lat: float) -> bytes:
    """Pack (lon, lat) into 21-byte Little-Endian Well-Known Binary (WKB) Point."""
    # 0x01: Little endian, 1: Point type (uint32), x: double, y: double
    return struct.pack("<BI2d", 1, 1, lon, lat)


def to_parquet(data: Any, path: str | Path, compression: str = "snappy") -> None:
    """Store municipal records as a compressed Parquet file."""
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as e:
        raise ImportError(
            "Parquet desteği için 'pyarrow' gereklidir. 'pip install pyarrow' veya "
            "'pip install izmir-open-data-py[data]' ile yükleyebilirsiniz."
        ) from e

    records = normalize_records(data)
    table = pa.Table.from_pylist(records)
    pq.write_table(table, str(path), compression=compression)


def read_parquet(path: str | Path) -> list[dict[str, Any]]:
    """Read records back from a Parquet file."""
    try:
        import pyarrow.parquet as pq
    except ImportError as e:
        raise ImportError(
            "Parquet desteği için 'pyarrow' gereklidir. 'pip install pyarrow' veya "
            "'pip install izmir-open-data-py[data]' ile yükleyebilirsiniz."
        ) from e

    table = pq.read_table(str(path))
    return table.to_pylist()


def to_geoparquet(
    data: Any,
    path: str | Path,
    geometry_column: str = "geometry",
    compression: str = "snappy",
) -> None:
    """Store municipal spatial records as a standard GeoParquet (v1.1.0) file with WKB Point geometry."""
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as e:
        raise ImportError(
            "GeoParquet desteği için 'pyarrow' gereklidir. 'pip install pyarrow' veya "
            "'pip install izmir-open-data-py[data]' ile yükleyebilirsiniz."
        ) from e

    records = normalize_records(data)
    enhanced_records = []
    bbox_xmin, bbox_ymin, bbox_xmax, bbox_ymax = (
        float("inf"),
        float("inf"),
        float("-inf"),
        float("-inf"),
    )
    has_valid_coords = False

    for rec in records:
        r = dict(rec)
        coords = extract_coordinates(r)
        if coords:
            lon, lat = coords
            r[geometry_column] = _point_to_wkb(lon, lat)
            bbox_xmin = min(bbox_xmin, lon)
            bbox_ymin = min(bbox_ymin, lat)
            bbox_xmax = max(bbox_xmax, lon)
            bbox_ymax = max(bbox_ymax, lat)
            has_valid_coords = True
        else:
            r[geometry_column] = None
        enhanced_records.append(r)

    table = pa.Table.from_pylist(enhanced_records)

    # GeoParquet v1.1.0 metadata
    col_metadata: dict[str, Any] = {
        "encoding": "WKB",
        "geometry_types": ["Point"],
        "crs": {
            "$schema": "https://proj.org/schemas/v0.7/projjson.schema.json",
            "type": "GeographicCRS",
            "name": "WGS 84",
            "id": {"authority": "EPSG", "code": 4326},
        },
    }
    if has_valid_coords:
        col_metadata["bbox"] = [bbox_xmin, bbox_ymin, bbox_xmax, bbox_ymax]

    geo_metadata = {
        "version": "1.1.0",
        "primary_column": geometry_column,
        "columns": {geometry_column: col_metadata},
    }

    existing_metadata = dict(table.schema.metadata or {})
    existing_metadata[b"geo"] = json.dumps(geo_metadata).encode("utf-8")
    table = table.replace_schema_metadata(existing_metadata)

    pq.write_table(table, str(path), compression=compression)
