from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from BasicMap import BasicMap

app = Dash(__name__)

# Federal Election 2022 Data
FedElection2022 = pd.read_csv('winnerdata.csv')
FedElection2022 = FedElection2022[FedElection2022['StateAb'] == "QLD"]

# Federal Electorate Boundaries
with open("australia_20.json") as json_file:
    FederalElectorates = json.load(json_file) 

# Brisbane City Council Election 2020 Data
BCCElection2020 = pd.read_csv('Council2020.csv')

# Brisbane City Council Ward Boundaries
with open("Ward_boundaries.geojson") as json_file:
    BCCWards = json.load(json_file) 


app.layout = html.Div([
    # Title
    html.H4('Interactive Map of the results of the 2020 Brisbane City Council Election'),
    html.P("Select an election to display:"),
    # Dropdown to select the election
    dcc.Dropdown(
        id='Election',
        options=["BCC2020", "Fed2022"],
        value="BCC2020",
        style={"width": "50%"}
        ),
    # Drop down to select booth data to display
    dcc.Dropdown(
        id='Booth Data',
        options=["BCC2020", "Fed2022"],
        value="BCC2020",
        style={"width": "50%"}
        ),

    # Radio button to select the election statistic to display
    dcc.RadioItems(
        id='Election Statistic', 
        options=["Winner", "Win Margin", "Green%", "Labor%", "Liberal%", "Independent%"],
        value="Winner",
        inline=True,
        # Move to the middle
        style={"float": "center", "display": "inline-block", "margin-left": "auto", "margin-right": "auto"}

    ),

    # Graph
    dcc.Graph(id="Election Statistic-graph", style={"height": 700})
])


@app.callback(
    # Output is the graph and the input is the dropdowns and radio buttons
    Output("Election Statistic-graph", "figure"), 
    Input("Election", "value"),
    Input("Booth Data", "value"),
    Input("Election Statistic", "value"))

def display_choropleth(election, booth, electionStatistic):
    # Set up the colourscales
    colourscales = {
            "Australian Labor Party": '#E2363E',
            "Liberal National Party of Queensland": '#2279f1',
            "Liberal": "#00529B",
            "The Nationals": "#397662",
            "The Greens": '#009b40',
            "Katter's Australian Party (KAP)": '#4E3524',
            "Independent": "#808080",
            "Centre Alliance": "#ff5800",
            "Government": '#E2363E',
            "Opposition": "#00529B",
            "Cross Bench": "#808080",
            "GRN" : '#009b40',
            "ALP" : '#E2363E',
            "LNP" : '#2279f1',
            "IND" : "#808080",
            "White" : "#ffffff",
            "Black" : "#000000",
            "Yellow" : "#ffff00"
    }

    # Brisbane City Council Election 2020
    if election == "BCC2020":
        # Create dependent on election statistic given
        if electionStatistic == "Winner":
            fig = px.choropleth_mapbox(BCCElection2020, geojson = BCCWards, locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", 
                                        color = "Winner Party", opacity=0.5, color_discrete_map=colourscales, 
                                        center={"lat": -27.4705, "lon": 153.0260}, zoom=9, hover_name="WARD", hover_data=["WARD", "Winner Party", "Hover Text"])
        elif electionStatistic == "Win Margin":
            fig = px.choropleth_mapbox(BCCElection2020, geojson = BCCWards, locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", 
                                    color = "Win Margin", opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales['Black']], 
                                    center={"lat": -27.4705, "lon": 153.0260}, zoom=9, hover_name="WARD", hover_data=["WARD", "Win Margin", "Hover Text"])
        else:
            # Create the abreviations
            abreviations = {"Green%" : "GRN", "Labor%" : "ALP", "Liberal%" : "LNP", "Independent%" : "IND"}
            party_name = abreviations[electionStatistic]
            party_per = party_name + "%"

            fig = px.choropleth_mapbox(BCCElection2020, geojson = BCCWards, locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", 
                                        color = party_per, opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales[party_name]], 
                                        center={"lat": -27.4705, "lon": 153.0260}, zoom=9, hover_name="WARD", hover_data=["WARD", party_per, "Hover Text"], 
                                        range_color=(0, 100))

        # Set the hoverlabel
        fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=8,
            font_family="Arial"
        ))

    # Federal Election 2022
    

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)