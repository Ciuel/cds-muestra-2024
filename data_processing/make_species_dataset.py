from pathlib import Path
import pandas as pd

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"

RESERVATIONS_PATH = DATA_PATH / "ocurrences_inside_reservations.csv"
SPECIES_PATH = DATA_PATH / "species.csv"
COLS = ["taxonKey","class","order","family", "verbatimScientificName", "vernacularName", "iucnRedListCategory", "image", "wikipedia_url"]

ocurrences = pd.read_csv(RESERVATIONS_PATH, encoding="utf-8", engine="c", low_memory=False, usecols=COLS)
species = ocurrences.drop_duplicates(subset=["taxonKey","verbatimScientificName"])
species.to_csv(SPECIES_PATH, index=False)