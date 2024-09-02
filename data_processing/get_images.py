import pandas as pd
from pathlib import Path
import requests
import json

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"
GBIF_PATH = DATA_PATH / "gbif"
ANIMALS_PATH = DATA_PATH / "ocurrences_inside_reservations.csv"

#curl -X GET --header 'Accept: application/json' 'https://api.inaturalist.org/v1/taxa?q={verbatimScientificName}&order=desc&order_by=observations_count'

def get_taxonkey_dict():
    if Path("taxonkey_dict_images.json").exists():
        with open("taxonkey_dict_images.json", "r") as json_file:
            return json.load(json_file)
    return {}

def get_images(animals_data):
    taxonkey_dict = get_taxonkey_dict()

    def save_dict_as_json(dictionary):
        if not Path("taxonkey_dict_images.json").exists():
            Path("taxonkey_dict_images.json").touch()
        with open("taxonkey_dict_images.json", "w") as json_file:
            json.dump(dictionary, json_file)

    def get_image(verbatimScientificName):
        print(verbatimScientificName)
        if verbatimScientificName in taxonkey_dict:
            print("Already in dict")
            return taxonkey_dict[verbatimScientificName]
        url = f"https://api.inaturalist.org/v1/taxa?q={verbatimScientificName}"
        print(url)
        response = requests.get(url)

        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            try:
                image_url = data["results"][0]["default_photo"]["square_url"].replace("square","original")
                taxonkey_dict[verbatimScientificName] = image_url
                print(image_url)
                save_dict_as_json(taxonkey_dict)  # Save the updated dict as a JSON file
                return image_url
            except:
                if not Path("missingimages.txt").exists():
                    Path("missingimages.txt").touch()
                print(f"No image for {verbatimScientificName}", file=open("missingimages.txt", "a"))
        return None



    animals_data["image"] = animals_data["verbatimScientificName"].apply(get_image)
    animals_data.to_csv(ANIMALS_PATH.with_name("ocurrences_inside_reservations.csv"), index=False, encoding="utf-8")

animals_data = pd.read_csv(ANIMALS_PATH, encoding="utf-8", engine="c", low_memory=False)
get_images(animals_data)
