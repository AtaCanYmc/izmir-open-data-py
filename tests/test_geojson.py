from izmir_open_data import extract_coordinates, to_geojson, to_geojson_feature


def test_extract_coordinates_cbs():
    item = {"Adi": "Kültürpark", "BOYLAM": 27.1428, "ENLEM": 38.4237}
    coords = extract_coordinates(item)
    assert coords == (27.1428, 38.4237)


def test_extract_coordinates_yazilim_sube():
    # LokasyonX = Latitude, LokasyonY = Longitude
    item = {"Adi": "Otobüs Durağı", "LokasyonX": "38.4192", "LokasyonY": "27.1287"}
    coords = extract_coordinates(item)
    # GeoJSON returns (longitude, latitude)
    assert coords == (27.1287, 38.4192)


def test_extract_coordinates_comma_decimal():
    item = {"Boylam": "27,1500", "Enlem": "38,4200"}
    coords = extract_coordinates(item)
    assert coords == (27.15, 38.42)


def test_extract_coordinates_invalid():
    assert extract_coordinates({}) is None
    assert extract_coordinates({"ENLEM": "invalid", "BOYLAM": "123"}) is None
    assert extract_coordinates({"ENLEM": 95, "BOYLAM": 27}) is None


def test_to_geojson_feature():
    poi = {
        "Adi": "Konak Meydanı",
        "Ilce": "Konak",
        "BOYLAM": 27.1287,
        "ENLEM": 38.4189,
    }
    feature = to_geojson_feature(poi)
    assert feature is not None
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "Point"
    assert feature["geometry"]["coordinates"] == [27.1287, 38.4189]
    assert feature["properties"]["Adi"] == "Konak Meydanı"


def test_to_geojson():
    raw_data = [
        {"Adi": "Nokta 1", "BOYLAM": 27.1, "ENLEM": 38.4},
        {"Adi": "Nokta 2", "BOYLAM": 27.2, "ENLEM": 38.5},
        {"Adi": "Koordinatsız Nokta"},
    ]
    fc = to_geojson(raw_data)
    assert fc["type"] == "FeatureCollection"
    assert len(fc["features"]) == 2
    assert fc["features"][0]["geometry"]["coordinates"] == [27.1, 38.4]
    assert fc["features"][1]["geometry"]["coordinates"] == [27.2, 38.5]

    wrapped = {"onemliyer": raw_data}
    fc_wrapped = to_geojson(wrapped)
    assert len(fc_wrapped["features"]) == 2
