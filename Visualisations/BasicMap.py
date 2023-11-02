import plotly.express as px
import pandas as pd
import json
# Import the colour scales from the ColourScales.py file
from COLOURSCALES import COLOURSCALE
from FILENAMES import FILENAME

def BasicMap(electionType: str, electionYear: str, hoverTextType: str, show: bool = True) -> None:

    file_names = FILENAME()[(electionType, electionYear)]
    # Read in the data
    data = pd.read_csv(file_names["winner"])
    # Read in the hover text
    HoverText = pd.read_csv(file_names["hovertext"])
    # Merge the data and the hover text
    data = pd.merge(data, HoverText, on="DivisionNm")

    # Read in the geojson file
    with open(file_names["boundaries"]) as json_file:
        locations = json.load(json_file)

    fig = px.choropleth_mapbox(data, geojson=locations,
                            color="PartyAb",
                            locations='DivisionNm',
                            featureidkey=file_names["featureidkey"],
                            hover_name="DivisionNm",
                            hover_data=[hoverTextType],
                            mapbox_style="carto-positron",
                            zoom=13,
                            center={"lat": -27.4705, "lon": 153.0260},
                            opacity=0.5,
                            color_discrete_map=COLOURSCALE())

    fig.update_layout(margin=dict(t=100, l=0, r=0, b=0))

    fig.update_layout(
        title=dict(text="Interactive Map of the results of the: " + electionYear + " " + electionType + " Election"),
        title_x=0.5,
    )
    if show:
        fig.show()
    name = "BasicMap" + electionType + electionYear + ".html"
    fig.write_html(name)

if __name__ == "__main__":
    BasicMap("Council", "2020",'HoverPrefDetailed')
    BasicMap("State", "2020", 'HoverPrefDetailed')
    BasicMap("Federal", "2022", 'HoverPrefDetailed')