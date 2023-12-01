from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from FILENAMES import FILENAME
from CENTRES import CENTRES
from BasicMap import BasicMap

# pale pastel green
BACKGROUND = "#C1E1C1"
# Set font to roboto
FONT = "Roboto"

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    style={
        'backgroundColor': BACKGROUND,
        'height': '100vh',
        'fontFamily': FONT,
    },
    children=[
        # Title
        html.H2('Interactive Map of the results', id='map-title', style={'text-align': 'center', 'fontFamily': FONT}),
        # RadioItems to select the election year
        dcc.RadioItems(
            id='Election',
            options=[
                {'label': 'Council 2020', 'value': 'Council 2020'},
                {'label': 'State 2020', 'value': 'State 2020'},
                {'label': 'Federal 2022', 'value': 'Federal 2022'}
            ],
            value='Council 2020',
            labelStyle={'display': 'inline-block', 'margin-right': '10px', 'fontFamily': FONT}
        ),
        # electorate dropdown
        html.Div(id="electorate-selection-dropdown"),
        # Textbox
        html.Div(id="electorate-hovertext")
    ]
)

# Create the electorate dropdown based on the selected election
@app.callback(
    Output("electorate-selection-dropdown", "children"),
    [Input("Election", "value")],
)
def create_electorate_dropdown(election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Create the dropdown
    return dcc.Dropdown(
        id="electorate-choosen",
        options=[{'label': electorate, 'value': electorate} for electorate in sorted(data['DivisionNm'].unique().tolist())],
        value=data['DivisionNm'].unique()[0],
        style={'width': '33%', 'fontFamily': FONT}
    )

# create the hovertext based on the selected electorate
@app.callback(
    Output("electorate-hovertext", "children"),
    [Input("electorate-choosen", "value"),
     Input("Election", "value")],
)
def create_electorate_hovertext(electorate, election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Get the hovertext for the selected electorate
    hovertext = data[data['DivisionNm'] == electorate]['HoverTPPDetailedstring'].values[0]
    # Create the textbox
    return dcc.Textarea(
        id="electorate-hovertext-textbox",
        value=hovertext,
        style={'width': '33%', 'height': '100vh', 'fontFamily': FONT}
    )

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)