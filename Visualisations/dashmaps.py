from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from BasicMap import BasicMap

# pale pastel green
BACKGROUND = "#C1E1C1"


app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': BACKGROUND, 'height': '100vh'}, children=[
    # Title
    html.H2('Interactive Map of the results'),
    # Graph
    dcc.Graph(id="Election Statistic-graph", style={"height": "calc(100vh - 100px)"}),
    html.P("Select an election to display:"),
    # Slider to select the election year
    dcc.Slider(
        id='Election',
        min=2017,
        max=2022,
        step=1,
        value=2020,
        marks={
            2021: {'label': 'State 2020'},
            2020: {'label': 'Council 2020'},
            2022: {'label': 'Federal 2022'}
        }
    )
])


@app.callback(
    # Output is the graph and the input is the slider
    Output("Election Statistic-graph", "figure"), 
    Input("Election", "value")
)

def display_choropleth(election):
    # get the election type and year from the slider
    election = {2021: ("State", "2020"), 2020: ("Council", "2020"), 2022: ("Federal", "2022")}[election]

    fig = BasicMap(election[0], election[1], 'HoverTPPDetailed', show=False)
    

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)