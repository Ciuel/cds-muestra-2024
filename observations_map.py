import geopandas as gpd
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import json
from map_constants import ANIMALS_PATH, AREAS_PATH, IUCN_COLORS, COLS, TYPES, ARGENMAP_STYLE
import os
import itertools

def make_map(gdf, filtered_data):
    gdf["id"] = gdf.index.astype(str)
    geojson_data = json.loads(gdf.to_json())

    fig = px.choropleth_mapbox(
        gdf,
        geojson=geojson_data,
        locations=gdf["id"],
        color=gdf["area"],
        color_continuous_scale="Viridis",
        range_color=(0, gdf["area"].max()),
        hover_name=gdf["fna"],
        opacity=0.2,
        mapbox_style=ARGENMAP_STYLE,
        center=dict(lon=-59.08574, lat=-46.83348),
        zoom=3,
    )

    years = filtered_data["year"].unique()
    years.sort()
    for i, year in enumerate(years):
        filtered_year_data = filtered_data[filtered_data["year"] == year]
        scatter_trace = go.Scattermapbox(
            ids=filtered_year_data["gbifID"],
            lat=filtered_year_data["decimalLatitude"],
            lon=filtered_year_data["decimalLongitude"],
            mode="markers",
            marker=go.scattermapbox.Marker(
                color=filtered_year_data["iucnRedListCategory"].map(IUCN_COLORS),
                size=15,
            ),
            hovertemplate="<b>%{text}</b><br><br>"
            + "Latitud: %{lat:.2f}<br>"
            + "Longitud: %{lon:.2f}<br>"
            + "Año: %{customdata[3]} <br>"
            + "Categoría IUCN: %{customdata[0]} <br>"
            + "Nombre vernacular: %{customdata[1]} <br>"
            + "<extra></extra>",
            text=filtered_year_data["verbatimScientificName"],
            customdata=filtered_year_data[
                ["iucnRedListCategory", "vernacularName", "verbatimScientificName", "year","image","wikipedia_url"]
            ].values,
            name=str(year),
            visible=False if i > 0 else True,
        )
        fig.add_trace(scatter_trace)

    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[
                {"visible": [True] + [False] * len(years)},  # Make geojson trace always visible
                {"title": "Year: " + str(year)},
                {"annotations": []},
            ],
            label=str(year),  # Add year label to the slider step
        )
        step["args"][0]["visible"][i+1] = True  # Make scatter traces invisible
        step["args"][2]["annotations"].append(
            dict(
                x=0.5,
                y=-0.1,
                xref="paper",
                yref="paper",
                text=str(year),
                showarrow=False,
            )
        )
        steps.append(step)

    sliders = [
        dict(
            active=0,
            currentvalue={"prefix": "Year: "},
            pad={"t": 50},
            steps=steps,
        )
    ]

    fig.update_layout(
        sliders=sliders,
        title="Year: " + str(years[0]),
        showlegend=False,
    )
    return fig


def make_maps(gdf,animals_data):
    import shutil
    pio.renderers.default = "browser"
    iucn_categories = animals_data["iucnRedListCategory"].unique()
    for i in range(len(iucn_categories)):
        if os.path.exists(os.path.join("maps",str(i+1))):
            shutil.rmtree(os.path.join("maps", str(i+1)))
    for i in range(len(iucn_categories)):
        if not os.path.exists(os.path.join("maps",str(i+1))):
            os.makedirs(os.path.join("maps",str(i+1)))
    for i in range(len(iucn_categories)):
        for combination in itertools.combinations(iucn_categories, i+1):
            file_name_combination = os.path.join("maps",str(i+1),"_".join(combination)+"_map")
            filtered_data = animals_data[animals_data["iucnRedListCategory"].isin(combination)]
            fig = make_map(gdf, filtered_data)
            fig.write_html(file_name_combination+".html", include_plotlyjs=True, include_mathjax="cdn")
            fig.write_json(file_name_combination+".json", pretty=True, remove_uids=False, engine='orjson')


if __name__ == '__main__':
    animals_data = pd.read_csv( ANIMALS_PATH, encoding="utf-8", engine="c", usecols=COLS, dtype=TYPES, low_memory=False,)

    gdf = gpd.read_file(AREAS_PATH).to_crs(4326)
    make_maps(gdf,animals_data)
