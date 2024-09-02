from shapely.geometry import Point
import geopandas as gpd
from pathlib import Path
from process_dataset import process_csv_chunked
from multiprocessing import freeze_support

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"

AREAS_PATH = DATA_PATH / "area_protegida.json"
ANIMALS_PATH = DATA_PATH / "animals_multimedia.csv"

areas = gpd.read_file(AREAS_PATH, encoding="utf-8")
areas["id"] = areas.index.astype(str)

def is_within(chunk):
    return chunk[chunk.apply(lambda row: any(areas.geometry.contains(Point(row["decimalLongitude"], row["decimalLatitude"]))), axis=1)]

def is_not_within(chunk):
    return chunk[chunk.apply(lambda row: not any(areas.geometry.contains(Point(row["decimalLongitude"], row["decimalLatitude"]))), axis=1)]

if __name__ == '__main__':
    freeze_support()
    process_csv_chunked(ANIMALS_PATH,DATA_PATH / "ocurrences_inside_reservations.csv", is_within, num_processes=8 )
    print("Done with inside")
    #process_csv_chunked(ANIMALS_PATH,DATA_PATH / "ocurrences_outside_reservations.csv", is_not_within, num_processes=8 )