from pathlib import Path

BASE_PATH = Path.cwd()
DATA_PATH = BASE_PATH / "datasets"

AREAS_PATH = DATA_PATH / "area_protegida.json"
ANIMALS_PATH = DATA_PATH / "ocurrences_inside_reservations.csv"

IUCN_COLORS = {
    "CR": "darkred",
    "EN": "red",
    "VU": "orange",
    "NT": "gold",
}

COLS = [
    "gbifID",
    "decimalLatitude",
    "decimalLongitude",
    "vernacularName",
    "verbatimScientificName",
    "iucnRedListCategory",
    "year",
    "image",
    "wikipedia_url",
]
TYPES = {
    "gbifID": int,
    "decimalLatitude": float,
    "decimalLongitude": float,
    "vernacularName": str,
    "verbatimScientificName": str,
    "iucnRedListCategory": str,
    "year": int,
    "image": str,
    "wikipedia_url": str,
}

ARGENMAP_STYLE = {
    "version": 8,
    "sources": {
        "argenmap": {
            "type": "raster",
            "scheme": "tms",
            "tiles": [
                "https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{y}.png"
            ],
            "tileSize": 256,
        }
    },
    "layers": [
        {
            "id": "imagery-tiles",
            "type": "raster",
            "source": "argenmap",
            "below": "waterway-label",
            "minzoom": 1,
            "maxzoom": 18,
        }
    ],
}