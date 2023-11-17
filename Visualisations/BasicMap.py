import plotly.express as px
import pandas as pd
import json
# Import the colour scales from the ColourScales.py file
from COLOURSCALES import COLOURSCALE
from FILENAMES import FILENAME
from CENTRES import CENTRES

BACKGROUND = "#C1E1C1"

def BasicMap(electionType: str, electionYear: str, hoverTextType: str, show: bool = True, centre_location_lat: float = -27.4705, centre_location_lon: float = 153.0260, centre_points: bool = False, show_legend: bool = False) -> px.choropleth_mapbox:

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
                            center={"lat": centre_location_lat, "lon": centre_location_lat},
                            opacity=0.5,
                            color_discrete_map=COLOURSCALE()
                                                        )

    if centre_points:
        centres = CENTRES()[electionType]
        for ward in centres:
            for center in centres[ward]:
                fig.add_scattermapbox(
                    lat=[center[1]],
                    lon=[center[0]],
                    mode="markers",
                    marker=dict(size=10, color="black"),
                    hoverinfo="text",
                    text=[ward],
                    showlegend=show_legend
                )


    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), plot_bgcolor=BACKGROUND, paper_bgcolor=BACKGROUND, font_family="Roboto", font_color="#000000")

    fig.update_layout(coloraxis_showscale=False)

    fig.update_traces(showlegend=show_legend)

    if show:
        fig.show()
    name = "BasicMap" + electionType + electionYear + ".html"
    fig.write_html(name)
    return fig

if __name__ == "__main__":
    BasicMap("Council", "2020",'HoverTPPDetailed', show=True, centre_points=True)
    # BasicMap("State", "2020", 'HoverTPPDetailed')
    # BasicMap("Federal", "2022", 'HoverTPPDetailed')