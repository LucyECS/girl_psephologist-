from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from BasicMap import BasicMap

# pale pastel green
BACKGROUND = "#C1E1C1"

figs = {}
for election in [("State", "2020"), ("Council", "2020"), ("Federal", "2022")]:
    figs[election] = BasicMap(election[0], election[1], 'HoverTPPDetailed', show=False, centre_points=True, show_legend=False)

# Set font to roboto
FONT = "Roboto"

app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': BACKGROUND, 'height': '100vh', 'fontFamily': FONT}, children=[
    # Title
    html.H2('Interactive Map of the results', id='map-title', style={'text-align': 'center', 'fontFamily': FONT}),
    html.P("Select an election to display:", style={'fontFamily': FONT}),
    # RadioItems to select the election year
    dcc.RadioItems(
        id='Election',
        options=[
            {'label': 'State 2020', 'value': 'State 2020'},
            {'label': 'Council 2020', 'value': 'Council 2020'},
            {'label': 'Federal 2022', 'value': 'Federal 2022'}
        ],
        value='Council 2020',
        labelStyle={'display': 'inline-block', 'margin-right': '10px', 'fontFamily': FONT}
    ),
    # Graph
    dcc.Graph(id="Election Statistic-graph", style={"height": "calc(100vh - 100px)", 'fontFamily': FONT}),
])


@app.callback(
    # Output is the graph and the input is the radioitems
    [Output("Election Statistic-graph", "figure"), Output('map-title', 'children')], 
    Input("Election", "value")
)

def display_choropleth(election):
    # get the election type and year from the radioitems
    election = tuple(election.split())

    fig = figs[election]
    
    # set the header based on the selected election type and year
    header = f'Interactive Map of {election[0]} {election[1]} Results'

    return fig, header


if __name__ == "__main__":
    app.run_server(debug=True)