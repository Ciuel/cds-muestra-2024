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
    exceptions = {
        "Grammostola vachoni":"https://es.wikipedia.org/wiki/Grammostola",
        "Andinagrion saliceti":"https://sib.gob.ar/especies/andinagrion-saliceti?tab=fuentes",
        "Myliobatis ridens":"https://www.inidep.edu.ar/especies/23-chucho-toro.html",
        "Euryades corethrus":"https://en.wikipedia.org/wiki/Euryades_corethrus",
    }
    dict = {}
    if Path("taxonkey_dict_wiki_links.json").exists():
        with open("taxonkey_dict_wiki_links.json", "r") as json_file:
            dict = json.load(json_file)
    dict.update(exceptions)
    return dict

def get_wiki_links(animals_data):

    taxonkey_dict = get_taxonkey_dict()

    def save_dict_as_json(dictionary):
        if not Path("taxonkey_dict_wiki_links.json").exists():
            Path("taxonkey_dict_wiki_links.json").touch()
        with open("taxonkey_dict_wiki_links.json", "w") as json_file:
            json.dump(dictionary, json_file)

    def get_wiki_link(verbatimScientificName):
        print(verbatimScientificName)
        if verbatimScientificName in taxonkey_dict:
            print("Already in dict")
            return taxonkey_dict[verbatimScientificName]
        url = f"https://es.wikipedia.org/wiki/{verbatimScientificName.replace(' ', '_')}"
        if requests.head(url).status_code == 200:
            wiki_link_url = url
            taxonkey_dict[verbatimScientificName] = wiki_link_url
            print(wiki_link_url)
            save_dict_as_json(taxonkey_dict)
            return wiki_link_url
        else:
            url = f"https://api.inaturalist.org/v1/taxa?q={verbatimScientificName}"
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                try:
                    wiki_link_url = data["results"][0]["wikipedia_url"]
                    taxonkey_dict[verbatimScientificName] = wiki_link_url
                    print(wiki_link_url)
                    save_dict_as_json(taxonkey_dict)  # Save the updated dict as a JSON file
                    return wiki_link_url
                except:
                    if not Path("missingwiki_links.txt").exists():
                        Path("missingwiki_links.txt").touch()
                    print(f"No wiki_link for {verbatimScientificName}", file=open("missingwiki_links.txt", "a"))
        return None



    animals_data["wikipedia_url"] = animals_data["verbatimScientificName"].apply(get_wiki_link)
    animals_data.to_csv(ANIMALS_PATH.with_name("ocurrences_inside_reservations.csv"), index=False, encoding="utf-8")

animals_data = pd.read_csv(ANIMALS_PATH, encoding="utf-8", engine="c", low_memory=False)
get_wiki_links(animals_data)
