import streamlit as st
import pandas as pd
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"
COLS = ["taxonKey", "verbatimScientificName", "vernacularName", "iucnRedListCategory", "image"]
IMAGE_SIZE = "small"
IUCN_CATEGORIES = {
    "CR": "En peligro crítico",
    "EN": "En peligro de extincíon",
    "VU": "Vulnerable",
    "NT": "Casi amenazado",
}


def initialize_state_variable(var_name, value):
    if var_name not in st.session_state:
        st.session_state[var_name] = value

def initialize_state_variables():
    initialize_state_variable("last_animals", [])
    initialize_state_variable("current_animals", [])
    initialize_state_variable("last_answer_correct", True)
    

def get_animals_sample():
    animals_data = pd.read_csv(DATA_PATH / "species.csv", encoding="utf-8", engine="c", low_memory=False, usecols=COLS)
    critical = animals_data[animals_data["iucnRedListCategory"] == "CR"]
    non_critical = animals_data[animals_data["iucnRedListCategory"] != "CR"]
    selected_non_critical = non_critical[~non_critical["verbatimScientificName"].isin(st.session_state["last_animals"])].sample(3, replace=False)
    selected_critical = critical[~critical["verbatimScientificName"].isin(st.session_state["last_animals"])].sample(1)
    selection = pd.concat([selected_non_critical, selected_critical])
    shuffled_selection = selection.sample(frac=1).reset_index(drop=True)
    st.session_state["current_animals"] = shuffled_selection

def header():
    st.title("¡Adivina el animal en peligro de extinción!")
    st.html("Todos estos animales están en peligro, pero uno de ellos está en peligro <span style='color:darkred'>crítico</span> de extinción. ¿Puedes adivinar cuál es?")


def select_animal(title, category):
    st.session_state["last_animals"] = st.session_state["current_animals"]

    with st._bottom:
        columns = st.columns([1,3,1])
        with columns[1]:
            if category == "CR":
                st.success(f"¡Correcto! {title} está en peligro crítico de extinción.")
                st.session_state["last_answer_correct"] = True
            else:
                st.error(f"{title} no está en peligro crítico de extinción, pero está {IUCN_CATEGORIES[category].lower()}.")
                st.session_state["last_answer_correct"] = False

def show_images():
    with st.spinner("Cargando imágenes"):
        animal_dict = {
            "images":     [image_url.replace("original", IMAGE_SIZE) for image_url in st.session_state["current_animals"]["image"].tolist()],
            "images_bytes": [],
            "titles":     st.session_state["current_animals"]["vernacularName"].tolist(),
            "categories": st.session_state["current_animals"]["iucnRedListCategory"].tolist(),
        }

        images = animal_dict["images"]
        titles = animal_dict["titles"]
        for image in images:
            response = requests.get(image)
            if response.status_code == 200:
                image = BytesIO(response.content)
                image = Image.open(image)
                image = image.resize((400, 300))
                animal_dict["images_bytes"].append(image)
            else:
                st.warning(f"Failed to download image: {image}")
        image_columns = st.columns(2)
        for i, image in enumerate(animal_dict["images_bytes"]):
            with image_columns[i % 2]:
                st.image(image, caption=str(titles[i]), width=400)
                st.button("Seleccionar", key=titles[i], on_click=select_animal, args=(titles[i],animal_dict["categories"][i]))
                st.markdown('<style>div.stButton > button:first-child {margin-left: auto; margin-right: auto; display: block;}</style>', unsafe_allow_html=True)
        st.session_state["animals_dict"] = animal_dict

def show_last_images():
    animal_dict = st.session_state["animals_dict"]
    image_columns = st.columns(2)
    for i, image in enumerate(animal_dict["images_bytes"]):
        with image_columns[i % 2]:
            st.image(image, caption=str(animal_dict["titles"][i]), width=400)
            st.button("Seleccionar", key=animal_dict["titles"][i], on_click=select_animal, args=(animal_dict["titles"][i],animal_dict["categories"][i]))
            st.markdown('<style>div.stButton > button:first-child {margin-left: auto; margin-right: auto; display: block;}</style>', unsafe_allow_html=True)
    


def main():
    columns = st.columns([1,3,1])
    with columns[1]:
        header()
        initialize_state_variables()
        if st.session_state["last_answer_correct"]:
            get_animals_sample()
            show_images()
        else:
            show_last_images()
main()