import plotly.express as px
import pandas as pd
import json
# Import the colour scales from the ColourScales.py file
from ColourScales import COLOURSCALE

# Read in the data
data = pd.read_csv('Election Results\State2020\created\State2020Winner.csv')
# Read in the hover text
HoverText = pd.read_csv('Election Results\State2020\created\State2020HoverText.csv')
# Merge the data and the hover text
data = pd.merge(data, HoverText, on="DivisionNm")

# Read in the geojson file
with open("Boundaries\State.geojson") as json_file:
    locations = json.load(json_file)

fig = px.choropleth_mapbox(data, geojson=locations,
                           color="PartyAb",
                           locations='DivisionNm',
                           featureidkey="properties.NAME",
                           hover_name="DivisionNm",
                           hover_data=["HoverText"],
                           mapbox_style="carto-positron",
                           zoom=5,
                           center={"lat": -27.5, "lon": 153},
                           opacity=0.5,
                           color_discrete_map=COLOURSCALE())

fig.update_layout(margin=dict(t=100, l=0, r=0, b=0))

fig.update_layout(
    title=dict(text="Interactive Map of the results of the 2020 State"),
    title_x=0.5
)

fig.show()
fig.write_html("Visualisations\Basic Map\StateWinnerMap.html")

