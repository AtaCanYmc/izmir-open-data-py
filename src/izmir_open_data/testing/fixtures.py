from typing import Any

# Realistic municipal datasets for offline testing and air-gapped CI environments
FIXTURES: dict[str, Any] = {
    "eczaneler": [
        {
            "Id": 101,
            "Adi": "Alsancak Eczanesi",
            "EczaneId": 101,
            "Telefon": "02324641122",
            "Adres": "Kıbrıs Şehitleri Cad. No:12/A",
            "Ilce": "KONAK",
            "LokasyonX": "38.4371",
            "LokasyonY": "27.1425",
            "NobetciMi": True,
        },
        {
            "Id": 102,
            "Adi": "Göztepe Eczanesi",
            "EczaneId": 102,
            "Telefon": "02322443344",
            "Adres": "Mithatpaşa Cad. No:450",
            "Ilce": "KONAK",
            "LokasyonX": "38.3985",
            "LokasyonY": "27.0982",
            "NobetciMi": False,
        },
    ],
    "bisim": {
        "kayit_sayisi": 2,
        "sayfa_numarasi": 1,
        "sayfa_basina_kayit_sayisi": 10,
        "toplam_sayfa_sayisi": 1,
        "kayitlar": [
            {
                "id": 1,
                "adi": "Alsancak İskele",
                "istasyon_no": 101,
                "kapasite": 20,
                "bos_bisiklet_sayisi": 8,
                "bos_park_sayisi": 12,
                "enlem": 38.4389,
                "boylam": 27.1394,
            },
            {
                "id": 2,
                "adi": "Konak İskele",
                "istasyon_no": 102,
                "kapasite": 24,
                "bos_bisiklet_sayisi": 14,
                "bos_park_sayisi": 10,
                "enlem": 38.4191,
                "boylam": 27.1283,
            },
        ],
    },
    "eshot_hatlar": [
        {
            "HAT_NO": 5,
            "HAT_ADI": "NARLIDERE - HALKAPINAR METRO",
            "GUZERGAH": "MİTHATPAŞA CADDESİ",
            "TARIFE": "Tam",
        },
        {
            "HAT_NO": 10,
            "HAT_ADI": "FAHRETTİN ALTAY - KONAK",
            "GUZERGAH": "İNÖNÜ CADDESİ",
            "TARIFE": "Tam",
        },
    ],
    "otoparklar": [
        {
            "id": 1,
            "name": "Alsancak Katlı Otoparkı",
            "capacity": 500,
            "occupancy": {
                "total": {"free": 120, "occupied": 380},
                "disabled": {"free": 8, "occupied": 2},
            },
            "lat": 38.435,
            "lng": 27.141,
        }
    ],
    "izsu_barajlar": [
        {
            "baraj_adi": "Tahtalı",
            "doluluk_orani": 32.45,
            "su_hacmi": 93500000,
            "tarih": "2026-11-20",
        },
        {
            "baraj_adi": "Balçova",
            "doluluk_orani": 48.12,
            "su_hacmi": 3700000,
            "tarih": "2026-11-20",
        },
    ],
    "tuvaletler": {
        "include_total": True,
        "resource_id": "d87de3c1-9bc0-4a8c-842a-90cd2a30d03a",
        "total": 2,
        "records": [
            {
                "_id": 1,
                "TESIS_ADI": "Kordon Akıllı Tuvalet",
                "ILCE": "KONAK",
                "MAHALLE": "ALSANCAK",
                "ADRES": "Atatürk Cad. 1. Kordon",
                "BOYLAM": 27.1398,
                "ENLEM": 38.4385,
            },
            {
                "_id": 2,
                "TESIS_ADI": "Göztepe Sahil Akıllı Tuvalet",
                "ILCE": "KONAK",
                "MAHALLE": "GÖZTEPE",
                "ADRES": "Mustafa Kemal Sahil Bulv.",
                "BOYLAM": 27.0985,
                "ENLEM": 38.3992,
            },
        ],
    },
    "itfaiye": {
        "include_total": True,
        "resource_id": "4b7a8da1-94ed-487f-8b7a-e13d40a5cd33",
        "total": 1,
        "records": [
            {
                "_id": 1,
                "YIL": 2026,
                "AY": 10,
                "KATEGORI": "YANGIN",
                "MUDAHALE_TIPI": "KONUT YANGINI",
                "MUDAHALE_YERI": "ALSANCAK",
                "ILCE": "KONAK",
                "MAHALLE": "KÜLTÜR",
                "MUDAHALE_ADEDI": 4,
            }
        ],
    },
    "izum": {
        "include_total": True,
        "resource_id": "a3bd880f-dfc6-4f65-bbfd-5fcc998268c3",
        "total": 1,
        "records": [
            {
                "_id": 1,
                "TARIH": "2026-11-20",
                "SAAT": "08:30",
                "BASLAMA": "Konak",
                "BITIS": "Karşıyaka",
                "HIZ": 42.5,
                "SURE": 18,
            }
        ],
    },
    "cbs_meydanlar": {
        "onemliyer": [
            {
                "Id": 1,
                "Adi": "Konak Meydanı",
                "Ilce": "Konak",
                "BOYLAM": 27.1287,
                "ENLEM": 38.4189,
            },
            {
                "Id": 2,
                "Adi": "Gündoğdu Meydanı",
                "Ilce": "Konak",
                "BOYLAM": 27.1402,
                "ENLEM": 38.4347,
            },
        ]
    },
}


def get_fixture(name: str) -> Any:
    """Retrieve a pre-recorded mock dataset by key."""
    if name not in FIXTURES:
        available = ", ".join(sorted(FIXTURES.keys()))
        raise KeyError(f"Bilinmeyen test verisi: '{name}'. Mevcut veriler: {available}")
    return FIXTURES[name]
