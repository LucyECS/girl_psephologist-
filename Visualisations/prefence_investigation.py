import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import csv


# Read in the data
results = pd.read_csv('Council2020.csv')


i = 0

values = [0]*24
print(values)



excl1 = (results["1 Party Excluded"][i], results["1GRN"][i], results["1ALP"][i], results["1LNP"][i], results["1IND"][i], results["1Exhausted"][i])
excl2 = (results["2 Party Excluded"][i], results["2GRN"][i], results["2ALP"][i], results["2LNP"][i], results["2IND"][i], results["2Exhausted"][i])
excl3 = (results["3 Party Excluded"][i], results["3GRN"][i], results["3ALP"][i], results["3LNP"][i], results["3IND"][i], results["3Exhausted"][i])


for excl in [excl1, excl2, excl3]:
    if excl[0] == "GRN":
        values[0] += excl[1]
        values[1] += excl[2]
        values[2] += excl[3]
        values[3] += excl[4]
        values[4] += excl[5]
    elif excl[0] == "ALP":
        values[5] += excl[1]
        values[6] += excl[2]
        values[7] += excl[3]
        values[8] += excl[4]
        values[9] += excl[5]
    elif excl[0] == "LNP":
        values[10] += excl[1]
        values[11] += excl[2]
        values[12] += excl[3]
        values[13] += excl[4]
        values[14] += excl[5]
    elif excl[0] == "IND":
        values[15] += excl[1]
        values[16] += excl[2]
        values[17] += excl[3]
        values[18] += excl[4]
        values[19] += excl[5]

values[20] = results["GRN Votes"]
values[21] = results["ALP Votes"]
values[22] = results["LNP Votes"]
values[23] = results["IND Votes"]


print(values)

    # Define the data for the sunburst chart
data = dict(
    party = ['GRN|GRN', 'GRN|ALP', 'GRN|LNP', 'GRN|IND', 'GRN|EXH', 'ALP|ALP', 'ALP|GRN', 'ALP|LNP', 'ALP|IND', 'ALP|EXH', 'LNP|LNP', 'LNP|GRN', 'LNP|ALP', 'LNP|IND', 'LNP|EXH', 'IND|IND', 'IND|GRN', 'IND|ALP', 'IND|LNP',  'IND|EXH', 'GRN', 'ALP', 'LNP', 'IND'],
    parent=['GRN', 'GRN', 'GRN', 'GRN', 'GRN', 'ALP', 'ALP', 'ALP', 'ALP', 'ALP', 'LNP', 'LNP', 'LNP', 'LNP', 'LNP', 'IND', 'IND', 'IND', 'IND', 'IND', '', '', '', ''],
    value = values
)

# # Create the sunburst chart
# fig = px.sunburst(
#     data,
#     names='party',
#     parents='parent',
#     values='value',
#     branchvalues="total",
# )


# # Set the margins for the chart
# fig.update_layout(margin=dict(t=100, l=0, r=0, b=0))

# fig.update_layout(
#     title=dict(text="Number of MPs elected to the House of Representatives by political party, showing position of party, 2022 Federal Election"),
#     title_x=0.5
# )

# # Show the sunburst chart
# fig.show()
# fig.write_html("Sunburst Chart.html")