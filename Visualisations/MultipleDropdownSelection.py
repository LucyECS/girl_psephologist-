from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from FILENAMES import FILENAME

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
        'display': 'flex',
    },
    children=[
    html.Div(
        ##### DIV 1 #####
        style={
            'backgroundColor': BACKGROUND,
            'height': '100vh',
            'width': '33%',
            'fontFamily': FONT,
            'display': 'inline-block',
        },
        children=[
            # Title
            html.H2(id='map-title1', style={'text-align': 'center', 'fontFamily': FONT}),
            # RadioItems to select the election year
            dcc.RadioItems(
                id='Election1',
                options=[
                    {'label': 'Council 2020', 'value': 'Council 2020'},
                    {'label': 'State 2020', 'value': 'State 2020'},
                    {'label': 'Federal 2022', 'value': 'Federal 2022'}
                ],
                value='Council 2020',
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'fontFamily': FONT}
            ),
            # electorate dropdown
            html.Div(id="electorate-selection-dropdown1"),
            # Textbox
            html.Div(id="electorate-hovertext1")
        ]
    ),
    
    html.Div(
        ##### DIV 2 #####
        style={
            'backgroundColor': BACKGROUND,
            'height': '100vh',
            'width': '33%',
            'fontFamily': FONT,
            'display': 'inline-block',
        },
        children=[
            # Title
            html.H2(id='map-title2', style={'text-align': 'center', 'fontFamily': FONT}),
            # RadioItems to select the election year
            dcc.RadioItems(
                id='Election2',
                options=[
                    {'label': 'Council 2020', 'value': 'Council 2020'},
                    {'label': 'State 2020', 'value': 'State 2020'},
                    {'label': 'Federal 2022', 'value': 'Federal 2022'}
                ],
                value='Council 2020',
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'fontFamily': FONT}
            ),
            # electorate dropdown
            html.Div(id="electorate-selection-dropdown2"),
            # Textbox
            html.Div(id="electorate-hovertext2")
        ]
    ),
    

    html.Div(
        ##### DIV 3 #####
        style={
            'backgroundColor': BACKGROUND,
            'height': '100vh',
            'width': '33%',
            'fontFamily': FONT,
            'display': 'inline-block',
        },
        children=[
            # Title
            html.H2(id='map-title3', style={'text-align': 'center', 'fontFamily': FONT}),
            # RadioItems to select the election year
            dcc.RadioItems(
                id='Election3',
                options=[
                    {'label': 'Council 2020', 'value': 'Council 2020'},
                    {'label': 'State 2020', 'value': 'State 2020'},
                    {'label': 'Federal 2022', 'value': 'Federal 2022'}
                ],
                value='Council 2020',
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'fontFamily': FONT}
            ),
            # electorate dropdown
            html.Div(id="electorate-selection-dropdown3"),
            # Textbox
            html.Div(id="electorate-hovertext3")
        ]
    ),
    ]
)


##### DIV 1 CALLBACKS #####
# Create the electorate dropdown based on the selected election
@app.callback(
    Output("electorate-selection-dropdown1", "children"),
    [Input("Election1", "value")],
)
def create_electorate_dropdown(election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Create the dropdown
    return dcc.Dropdown(
        id="electorate-choosen1",
        options=[{'label': electorate, 'value': electorate} for electorate in sorted(data['DivisionNm'].unique().tolist())],
        value=data['DivisionNm'].unique()[0],
        style={'width': '100%', 'fontFamily': FONT}
    )

# create the hovertext based on the selected electorate
@app.callback(
    Output("electorate-hovertext1", "children"),
    [Input("electorate-choosen1", "value"),
     Input("Election1", "value")],
)
def create_electorate_hovertext(electorate, election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Get the hovertext for the selected electorate
    hovertext = data[data['DivisionNm'] == electorate]['HoverTPPDetailedstring'].values[0]
    # Create the textbox
    return dcc.Textarea(
        id="electorate-hovertext-textbox1",
        value=hovertext,
        style={'width': '100%', 'height': '100vh', 'fontFamily': FONT}
    )

##### DIV 2 CALLBACKS #####
# Create the electorate dropdown based on the selected election
@app.callback(
    Output("electorate-selection-dropdown2", "children"),
    [Input("Election2", "value")],
)
def create_electorate_dropdown(election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Create the dropdown
    return dcc.Dropdown(
        id="electorate-choosen2",
        options=[{'label': electorate, 'value': electorate} for electorate in sorted(data['DivisionNm'].unique().tolist())],
        value=data['DivisionNm'].unique()[0],
        style={'width': '100%', 'fontFamily': FONT}
    )

# create the hovertext based on the selected electorate
@app.callback(
    Output("electorate-hovertext2", "children"),
    [Input("electorate-choosen2", "value"),
     Input("Election2", "value")],
)
def create_electorate_hovertext(electorate, election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Get the hovertext for the selected electorate
    hovertext = data[data['DivisionNm'] == electorate]['HoverTPPDetailedstring'].values[0]
    # Create the textbox
    return dcc.Textarea(
        id="electorate-hovertext-textbox2",
        value=hovertext,
        style={'width': '100%', 'height': '100vh', 'fontFamily': FONT}
    )

##### DIV 3 CALLBACKS #####
# Create the electorate dropdown based on the selected election
@app.callback(
    Output("electorate-selection-dropdown3", "children"),
    [Input("Election3", "value")],
)
def create_electorate_dropdown(election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Create the dropdown
    return dcc.Dropdown(
        id="electorate-choosen3",
        options=[{'label': electorate, 'value': electorate} for electorate in sorted(data['DivisionNm'].unique().tolist())],
        value=data['DivisionNm'].unique()[0],
        style={'width': '100%', 'fontFamily': FONT}
    )

# create the hovertext based on the selected electorate
@app.callback(
    Output("electorate-hovertext3", "children"),
    [Input("electorate-choosen3", "value"),
     Input("Election3", "value")],
)
def create_electorate_hovertext(electorate, election):
    # Load the data
    data = pd.read_csv(FILENAME()[election.split()[0], election.split()[1]]['hovertext'])
    # Get the hovertext for the selected electorate
    hovertext = data[data['DivisionNm'] == electorate]['HoverTPPDetailedstring'].values[0]
    # Create the textbox
    return dcc.Textarea(
        id="electorate-hovertext-textbox3",
        value=hovertext,
        style={'width': '100%', 'height': '100vh', 'fontFamily': FONT}
    )

##### UPDATE MAP TITLE CALLBACKS #####
# Update the map title based on the selected electorate in DIV 1
@app.callback(
    Output("map-title1", "children"),
    [Input("electorate-choosen1", "value")]
)
def update_map_title1(electorate):
    return electorate

# Update the map title based on the selected electorate in DIV 2
@app.callback(
    Output("map-title2", "children"),
    [Input("electorate-choosen2", "value")]
)
def update_map_title2(electorate):
    return electorate

# Update the map title based on the selected electorate in DIV 3
@app.callback(
    Output("map-title3", "children"),
    [Input("electorate-choosen3", "value")]
)
def update_map_title3(electorate):
    return electorate

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)