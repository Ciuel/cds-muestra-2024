import pandas as pd
from pathlib import Path
import requests
import json

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"
GBIF_PATH = DATA_PATH / "gbif"
ANIMALS_PATH = DATA_PATH / "ocurrences_inside_reservations.csv"
#curl -X 'GET' 'https://api.gbif.org/v1/species/{taxonKey}/vernacularNames' -H 'accept: application/json'



def get_taxonkey_dict():
    if Path("taxonkey_dict_names.json").exists():
        with open("taxonkey_dict_names.json", "r") as json_file:
            return json.load(json_file)
    return {}

def get_vernacular_names(animals_data):
    exceptions = {
        "11041256":"Semillero del Iberá",
        "2437619": "Mara Patagónica",
        "2153726": "Tarántula Argentina",
        "10856092":"Ranita de la Hojarasca Confundida",
        "5141258":"Aceitosa del litoral",
        "5216368":"Tiburón espinoso",
        "5141257": "Aceitosa Arlequín",
        "5215514":"Torpedo Argentino",
        "1423514":"Libelula del delta",
        "2422150":"Sapo Correntino",

    }
    taxonkey_dict = get_taxonkey_dict()
    
    def save_dict_as_json(dictionary):
        if not Path("taxonkey_dict_names.json").exists():
            with open("taxonkey_dict_names.json", "w") as json_file:
                json.dump({}, json_file)
        with open("taxonkey_dict_names.json", "r") as json_file:
            json_dict = json.load(json_file)
            json_dict.update(dictionary)
        with open("taxonkey_dict_names.json", "w") as json_file:
            json.dump(json_dict, json_file)

    def get_vernacular_name(taxon_key):
        if str(taxon_key) in exceptions.keys():
                taxonkey_dict[str(taxon_key)] = exceptions[str(taxon_key)]
                save_dict_as_json(taxonkey_dict)
                return exceptions[str(taxon_key)]
        if str(taxon_key) in taxonkey_dict.keys():
            print("Already in dict")
            print(taxonkey_dict[str(taxon_key)])
            return taxonkey_dict[str(taxon_key)]
        url = f"https://api.gbif.org/v1/species/{taxon_key}/vernacularNames"
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            vernacular_names = data["results"]
            spanish_names = [name["vernacularName"] for name in vernacular_names if name["language"] == "spa"]
            english_names = [name["vernacularName"] for name in vernacular_names if name["language"] == "eng"]
            print(spanish_names)
            if spanish_names:
                taxonkey_dict[taxon_key] = spanish_names[0].title()
                save_dict_as_json(taxonkey_dict)
                name = spanish_names[0]
            elif english_names:
                taxonkey_dict[taxon_key] = english_names[0].title()
                save_dict_as_json(taxonkey_dict)
                name = english_names[0]
            else:
                with open("missingnames.txt", "a") as file:
                    file.write(str(taxon_key) + "\n")
                name = ""
                return name
            return name

        return None

    animals_data["vernacularName"] = animals_data["taxonKey"].apply(get_vernacular_name)
    animals_data["vernacularName"] = animals_data["vernacularName"].str.replace('""', ' ')
    animals_data["vernacularName"] = animals_data["vernacularName"].str.replace('"', '')
    animals_data["vernacularName"] = animals_data["vernacularName"].str.replace('|', ' ')
    animals_data["vernacularName"] = animals_data["vernacularName"].str.replace("'", ' ')
    animals_data.to_csv(ANIMALS_PATH.with_name("ocurrences_inside_reservations.csv"), index=False, encoding="utf-8")

def second_pass(animals_data):
    def inner_second_pass(taxon_key):
        taxonkey_dict = get_taxonkey_dict()
        if taxon_key in taxonkey_dict:
            print( taxonkey_dict[taxon_key])
            return taxonkey_dict[taxon_key]
        else:
            print(taxon_key)
        return ""
    
    animals_data["vernacularName"] = animals_data["taxonKey"].apply(inner_second_pass)

animals_data = pd.read_csv(ANIMALS_PATH, encoding="utf-8", engine="c", low_memory=False)
get_vernacular_names(animals_data)