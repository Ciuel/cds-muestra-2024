
import streamlit as st
from pathlib import Path
import plotly.io as pio
import streamlit.components.v1 as stc
import json

BASE_PATH = Path.cwd().parent
DATA_PATH = BASE_PATH / "datasets"
MAPS_PATH = BASE_PATH / "maps"
CATEGORIES_DICT = {
    "CR": {"name": "peligro crítico","desc":"se considera que se está enfrentando a un riesgo de extinción extremadamente alto en estado de vida silvestre"},
    "EN": {"name": "en peligro","desc":"se considera que se está enfrentando a un riesgo de extinción muy alto en estado de vida silvestre"},
    "VU": {"name": "vulnerable","desc":"se considera que se está enfrentando a un riesgo de extinción alto en estado de vida silvestre"},
    "NT": {"name": "casi amenazado","desc":"está próximo a satisfacer los criterios para peligro crítico, peligro o vulnerable, o posiblemente los satisfaga, en un futuro cercano"},
}

st.title("Animales en peligro de extinción 1994-2024")
st.html("De acuerdo a la IUCN actualmente en Argentina hay <span style='color:darkred'>52</span> especies de animales en estado crítico, <span style='color:red'>101</span> en peligro, <span style='color:orange'>156</span> vulnerables y <span style='color:gold'>146</span> cerca de entrar en peligro.")
st.markdown("Este mapa muestra la ubicación de los avistamientos animales en peligro de extinción en Argentina entre 1994 y 2024.")
st.markdown("")

@st.cache_resource
def load_maps():
    figure_files = MAPS_PATH.glob("**/*.json")
    figures = {}
    for file in figure_files:
        with open(file, "r") as f:
            figures[file.name] = pio.from_json(json.dumps(json.load(f)))
    return figures

def make_observation_section(point):
    with st.container(border=True):
        st.title(f"Seleccionaste al {point['customdata'][1]}")
        st.markdown(f"El {point['customdata'][1]} es un animal en peligro de extinción de la categoría {CATEGORIES_DICT[point['customdata'][0]]['name']}, esto significa que {CATEGORIES_DICT[point['customdata'][0]]['desc']}.")
        with st.columns((1,3,1))[1]:
            st.image(point["customdata"][4].replace("original", "small"), width=300)
    with st.container(border=True):
        stc.iframe(point["customdata"][5], height=800, scrolling=True)

def make_area_section(point):
    with st.container(border=True):
        st.markdown(f"Seleccionaste el área de protegida {point['hovertext']}, selecciona un punto para ver el avistamiento correspondiente.")


maps = load_maps()
columns = st.columns(2)
with columns[0]:
    st.markdown("En el mapa se ven 4 categorías de la lista roja de la IUCN:")
    selected_checkboxes = []
    if st.checkbox("En peligro crítico mostrado en rojo oscuro", value=True, key="CR"):
        selected_checkboxes.append("CR")
    if st.checkbox("En peligro mostrado en rojo", value=True, key="EN"):
        selected_checkboxes.append("EN")
    if st.checkbox("Vulnerable mostrado en naranja", value=True, key="VU"):
        selected_checkboxes.append("VU")
    if st.checkbox("Casi amenazado mostrado en amarillo", value=True, key="NT"):
        selected_checkboxes.append("NT")

    if len(selected_checkboxes) == 0:
        st.error("Seleccione al menos una categoría de la lista roja de la IUCN.")
        st.stop()

    selected_checkboxes.sort(reverse=True)
    map_name = "_".join(selected_checkboxes) + "_map.json"
    fig = maps[map_name]
    fig.update_layout(width=2000,height=1100,mapbox_zoom=3.7, mapbox_center={"lat": -42.3, "lon": -66.284489})
    event = st.plotly_chart(fig ,width=1000, key="ids",selection_mode="points", on_select="rerun", )
with columns[1]:
    if event.selection.points != []:
        point = event.selection.points[0]
        try:
            make_observation_section(point)
        except KeyError:
            try:
                make_area_section(point)
            except KeyError:
                st.markdown("Oops")
    else:
        st.markdown("Seleccione un punto en el mapa para ver la imagen y la información del animal.")

