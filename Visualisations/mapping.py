import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import csv




df = pd.read_csv('winnerdata.csv')
with open("australia_20.json") as json_file:
    abr = json.load(json_file) 

# Only map queensland
df = df[df['StateAb'] == "QLD"]


# Read in the data
results = pd.read_csv('Council2020.csv')
with open("Ward_boundaries.geojson") as json_file:
    geo = json.load(json_file) 

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

def mapping_results(type):
    # Create dependent on type given
    if type == "GRN":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "GRN%", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales['GRN']], 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "GRN%", "Hover Text"], range_color=(0, 100))
    elif type == "ALP":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "ALP%", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales['ALP']], 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "ALP%", "Hover Text"], range_color=(0, 100))
    elif type == "LNP":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "LNP%", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales['LNP']], 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "LNP%", "Hover Text"], range_color=(0, 100))
    elif type == "IND":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "IND%", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_continuous_scale=[colourscales['White'], colourscales['IND']], 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "IND%", "Hover Text"], range_color=(0, 100))
    elif type == "Winner":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "Winner Party", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_discrete_map=colourscales, 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "Winner", "Hover Text"])
    elif type == "Win Margin":
        fig = px.choropleth_mapbox(results, geojson=geo, color = "Win Margin", locations='WARD', featureidkey="properties.WARD", mapbox_style= "carto-positron", opacity=0.5, color_continuous_scale=[colourscales['Black'], colourscales['Yellow']], 
                                   center={"lat": -27.4705, "lon": 153.0260}, zoom=10, hover_name="WARD", hover_data=["WARD", "Win Margin", "Hover Text"])

    for i, winner in enumerate(df['PartyNm'].unique()):
        dfp = df[df['PartyNm'] == winner]
        print(winner)
        fig.add_choroplethmapbox(geojson=abr, locations=dfp['DivisionNm'],
                                z=[i,] * len(dfp), featureidkey="properties.electorateName",
                                showlegend=True, name=winner, 
                                text = ("Division Name: " + dfp['DivisionNm'] + ",  MP Name : " + dfp["GivenNm"] + " " + dfp["Surname"]), 
                                hoverinfo= "name+text",
                                marker_opacity=0.05, marker_line_width=3, marker_line_color=colourscales[winner],
                                colorscale=((0.0, colourscales[winner]), (1.0, colourscales[winner])), showscale=False)

    fig.update_layout(margin=dict(t=100, l=0, r=0, b=0))

    fig.update_layout(
        title=dict(text="Interactive Map of the results of the 2020 Brisbane City Council Election"),
        title_x=0.5
    )

    fig.show()
    fig.write_html("Choropleth Map.html")

mapping_results("Winner")