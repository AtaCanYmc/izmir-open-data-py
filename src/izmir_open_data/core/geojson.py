from typing import Any


def _parse_coordinate(val: Any) -> float | None:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        cleaned = val.strip().replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def extract_coordinates(item: Any) -> tuple[float, float] | None:
    """Extract coordinates from municipal data and return (longitude, latitude) [lon, lat]."""
    if not isinstance(item, dict):
        return None

    lon: float | None = None
    lat: float | None = None

    # 1. CBS format (BOYLAM / ENLEM)
    if "BOYLAM" in item and "ENLEM" in item:
        lon = _parse_coordinate(item["BOYLAM"])
        lat = _parse_coordinate(item["ENLEM"])
    elif "boylam" in item and "enlem" in item:
        lon = _parse_coordinate(item["boylam"])
        lat = _parse_coordinate(item["enlem"])
    elif "Boylam" in item and "Enlem" in item:
        lon = _parse_coordinate(item["Boylam"])
        lat = _parse_coordinate(item["Enlem"])
    # 2. Yazılım Şube and Eczaneler (LokasyonX: Latitude, LokasyonY: Longitude)
    elif "LokasyonX" in item and "LokasyonY" in item:
        lat = _parse_coordinate(item["LokasyonX"])
        lon = _parse_coordinate(item["LokasyonY"])
    elif "KoordinatX" in item and "KoordinatY" in item:
        lat = _parse_coordinate(item["KoordinatX"])
        lon = _parse_coordinate(item["KoordinatY"])
    # 3. Standard English (latitude / longitude)
    elif "latitude" in item and "longitude" in item:
        lat = _parse_coordinate(item["latitude"])
        lon = _parse_coordinate(item["longitude"])
    elif "lat" in item and ("lng" in item or "lon" in item):
        lat = _parse_coordinate(item["lat"])
        lon = _parse_coordinate(item.get("lng") if "lng" in item else item.get("lon"))

    if (
        lon is not None
        and lat is not None
        and -180.0 <= lon <= 180.0
        and -90.0 <= lat <= 90.0
    ):
        return (lon, lat)

    return None


def to_geojson_feature(item: Any) -> dict[str, Any] | None:
    """Convert a single record into a GeoJSON Feature."""
    coords = extract_coordinates(item)
    if not coords:
        return None

    properties = dict(item) if isinstance(item, dict) else {}
    feature: dict[str, Any] = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": list(coords),
        },
        "properties": properties,
    }

    feature_id = (
        properties.get("Id")
        or properties.get("ID")
        or properties.get("id")
        or properties.get("_id")
        or properties.get("IstasyonId")
        or properties.get("EczaneId")
    )
    if feature_id is not None:
        feature["id"] = feature_id

    return feature


def to_geojson(data: Any) -> dict[str, Any]:
    """Convert municipal data list or wrapper into a standard GeoJSON FeatureCollection."""
    items: list[Any] = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get("onemliyer"), list):
            items = data["onemliyer"]
        elif isinstance(data.get("records"), list):
            items = data["records"]
        elif isinstance(data.get("kayitlar"), list):
            items = data["kayitlar"]

    features = []
    for item in items:
        feat = to_geojson_feature(item)
        if feat is not None:
            features.append(feat)

    return {
        "type": "FeatureCollection",
        "features": features,
    }
