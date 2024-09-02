import pandas as pd
from pathlib import Path
from process_dataset import process_csv_chunked
from multiprocessing import freeze_support
import zipfile

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"
GBIF_PATH = DATA_PATH / "gbif"

COLUMNS = ["gbifID","catalogNumber","year","month","day","eventTime","decimalLongitude","decimalLatitude","class","order","family","verbatimScientificName","vernacularName","taxonKey","level1Name","level2Name","iucnRedListCategory"]

NO_NA_COLUMNS = ["gbifID","catalogNumber","year","month","day","decimalLongitude","decimalLatitude","class","order","family","verbatimScientificName","taxonKey","level1Name","level2Name","iucnRedListCategory"]

EXCEPTIONS = {
    "Haematopus ostralegus Linnaeus, 1758": "Haematopus ostralegus",
    "Laterallus spiloptera": "Laterallus spilonota",
    "Sympterygia bonapartei":
    "Torpedo puelcha"
}

def cut(chunk):
    chunk= chunk.dropna(subset=NO_NA_COLUMNS, inplace=False)
    chunk.loc[chunk["verbatimScientificName"] == "Haematopus ostralegus Linnaeus, 1758", "verbatimScientificName"] = "Haematopus ostralegus"
    chunk.loc[chunk["verbatimScientificName"] == "Laterallus spiloptera", "verbatimScientificName"] = "Laterallus spilonota"
    chunk.loc[chunk["verbatimScientificName"] == "Sympterygia bonapartei", "verbatimScientificName"] = "Sympterygia bonapartii"
    chunk.loc[chunk["verbatimScientificName"] == "Torpedo puelcha", "verbatimScientificName"] = "Tetronarce puelcha"
    return chunk

media_df = pd.read_csv(GBIF_PATH / "multimedia.txt", encoding="utf-8", engine='c', delimiter="\t", usecols=["gbifID","identifier"], low_memory=False)
media_df.rename(columns={"identifier":"image"}, inplace=True)
def merge(chunk):
    return pd.merge(chunk, media_df, on="gbifID", how="left")



if __name__ == '__main__':
    # Decompress the folder
    with zipfile.ZipFile(DATA_PATH / "gbif.zip", 'r') as zip_ref:
        zip_ref.extractall(DATA_PATH)
    freeze_support()
    process_csv_chunked(GBIF_PATH / "occurrence.txt", DATA_PATH / "animals_filtered.csv", cut,read_kwargs={"usecols":COLUMNS,"delimiter":"\t"} )
    process_csv_chunked(DATA_PATH / "animals_filtered.csv", DATA_PATH / "animals_multimedia.csv", merge, read_kwargs={"usecols":COLUMNS},num_processes=8)