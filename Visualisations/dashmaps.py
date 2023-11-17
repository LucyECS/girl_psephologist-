from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from FILENAMES import FILENAME
from CENTRES import CENTRES
from BasicMap import BasicMap

# pale pastel green
BACKGROUND = "#C1E1C1"

figs = {}
electorates = {}
for election in [("State", "2020"), ("Council", "2020"), ("Federal", "2022")]:
    figs[election] = BasicMap(election[0], election[1], 'HoverTPPDetailedBr', show=False, centre_points=False, show_legend=False)
    electorates[election[0]] = figs[election].data[0].locations

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
        # Graph
        dcc.Graph(id="Election Statistic-graph", style={"height": "calc(100vh - 200px)", 'fontFamily': FONT}),
        # Hover text dropdown with the electorates as options depending on the chosen election with the default value being the first electorate
        html.Div(id="electorate-selection-dropdown", style={'fontFamily': FONT}),
    ]
)


# Create the electorate dropdown based on the selected election
@app.callback(
    [Output("electorate-selection-dropdown", "children"),
     Output("electorate-choosen", "value")],
    [Input("Election", "value"),
     Input("Election Statistic-graph", "clickData")],
     supress_callback_exceptions=True
)
def update_electorate_dropdown(election, click_data, suppress_callback_exceptions=True):
    if click_data:
        choosen_electorate = click_data['points'][0]['location']
    else:
        choosen_electorate = electorates[election[0]][0]
    electorate_selection_dropdown = None
    # get the election type and year from the radioitems
    election = tuple(election.split())
    # get the electorates for the selected election
    electorates = electorates[election[0]]
    # return the dropdown with the electorates as options depending on the chosen election with the default value being the first electorate
    electorate_selection_dropdown = dcc.Dropdown(
        id="electorate-dropdown",
        options=[{'label': electorate, 'value': electorate} for electorate in electorates],
        value=choosen_electorate,
        style={'fontFamily': FONT}
    )
    return electorate_selection_dropdown, choosen_electorate



# Update the graph and the header based on the selected election
@app.callback(
    # Output is the graph, the header, and the clicked electorate information
    [Output("Election Statistic-graph", "figure"), 
     Output('map-title', 'children')], 
    [Input("Election", "value"),
     Input("electorate-choosen", "value")],
        suppress_callback_exceptions=True
)
def display_choropleth(election, electorate_choosen, suppress_callback_exceptions=True):
    # get the election type and year from the radioitems
    election = tuple(election.split())
    electorate = electorate_choosen
    elec_lat = CENTRES()[election[0]][electorate][0][1]
    elec_lon = CENTRES()[election[0]][electorate][0][0]

    fig = BasicMap(election[0], election[1], 'HoverTPPDetailedBr', show=False, centre_points=False, show_legend=False, centre_location_lat=elec_lat, centre_location_lon=elec_lon)
    
    # set the header based on the selected election type and year
    header = f'Interactive Map of {election[0]} {election[1]} Results - Clicked on {electorate}'

    return fig, header
    



# # Update the graph and the header based on the selected election
# @app.callback(
#     # Output is the graph, the header, and the clicked electorate information
#     [Output("Election Statistic-graph", "figure"), 
#      Output('map-title', 'children'), 
#      Output("clicked-info", "children")], 
#     [Input("Election", "value"), 
#      Input("Election Statistic-graph", "clickData")]
# )
# def display_choropleth(election, click_data):
#     # get the election type and year from the radioitems
#     election = tuple(election.split())

#     fig = figs[election]
    
#     # set the header based on the selected election type and year
#     header = f'Interactive Map of {election[0]} {election[1]} Results'

#     clicked_info = None

#     # check if click data is available
#     if click_data:
#         # get the clicked point information
#         point_info = click_data['points'][0]
#         # update the header with the clicked point information
#         header += f" - Clicked on {point_info['location']}"
#         # get the HoverTPPDetailed information for the clicked electorate
#         clicked_info = get_hover_tpp_detailed(point_info['location'], election)  # Replace this with your function to get HoverTPPDetailed information

#     return fig, header, clicked_info

# # Helper function to get the HoverTPPDetailed information for the clicked electorate
# def get_hover_tpp_detailed(electorate, election, HoverTextType: str = 'HoverTPPDetailedstring'):
#     # Replace this with your code to retrieve the HoverTPPDetailed information for the clicked electorate
#     # import hover text types
#     file_names = FILENAME()[(election[0], election[1])]
#     HoverText = pd.read_csv(file_names["hovertext"])
#     # get the HoverTPPDetailed information for the clicked electorate
#     hover_text = HoverText[HoverText['DivisionNm'] == electorate][HoverTextType].iloc[0]
#     return dcc.Markdown(hover_text, style={'fontFamily': FONT, 'backgroundColor': 'white', 'maxHeight': '200px'})


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)