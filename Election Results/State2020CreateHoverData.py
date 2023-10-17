import csv

header = ["DivisionNm", "HoverText"]

#  Example Hover Text
"""
Division Information
Division Name: Brisbane
Winner: Queensland Greens (Stephen, BATES)
Number of Candidates: 7
Number of Formal Votes: 111110
Number of Informal Votes: 2312 (2.08%)

Primary Votes
AJP:    2135 (1.96%)
UAPP:   2102 (1.93%)
GRN:    29641 (27.24%)
ALP:    29652 (27.25%)
LNP:    41032 (37.71%)
ON:     2429 (2.23%)
LDP:    1807 (1.66%)
"""

HoverText = {}

# Read through Federal2022FirstPrefsByPollingPlace.csv
with open("Election Results\State2020\created\State2020FirstPref.csv") as results:
    # object to DictReader method 
    reader_obj = csv.DictReader(results)

    # create rows
    rows = []

    for row in reader_obj:
        rows.append(row)

    # Get unique Division Names
    DivisionNames = []
    for row in rows:
        if row["DivisionNm"] not in DivisionNames:
            DivisionNames.append(row["DivisionNm"])

    # Iterate through each Division
    for division in DivisionNames:

        # Initialise variables
        hovertext = ""
        totalvotes = 0
        informalvotes = 0
        numberofcandidates = -1
        winner = ""

        # Iterate through each row
        for row in rows:
            if row["DivisionNm"] == division:
                totalvotes = totalvotes + int(row["TotalVotes"])
                numberofcandidates = numberofcandidates + 1
                if row["Surname"] == "Informal":
                    informalvotes = informalvotes + int(row["TotalVotes"])
                if row["Elected"] == "Y":
                    winner = row["PartyNm"] + " (" + row["GivenNm"] + ", " + row["Surname"] + ")"
        hovertext = hovertext + "Division Information" + "<br>"
        hovertext = hovertext + "Division Name: " + division + "<br>"
        hovertext = hovertext + "Winner: " + winner + "<br>"
        hovertext = hovertext + "Number of Candidates: " + str(numberofcandidates) + "<br>"
        hovertext = hovertext + "Number of Formal Votes: " + str(totalvotes) + "<br>"
        hovertext = hovertext + "Number of Informal Votes: " + str(informalvotes) + " (" + str(round(informalvotes*100/totalvotes, 2)) + "%" + ")" + "<br>"
        hovertext = hovertext + "---------------------------------" + "<br>"
        hovertext = hovertext + "Primary Votes" + "<br>"
        for row in rows:
            if row["DivisionNm"] == division:
                if row["Surname"] != "Informal":
                    hovertext = hovertext + row["PartyAb"] + ": \t" + str(row["TotalVotes"]) + " (" + str(round(int(row["TotalVotes"])*100/(totalvotes-informalvotes), 2)) + "%" + ")" + "<br>"
        HoverText[division] = hovertext

# Write to Federal2022HoverText.csv
with open("Election Results\State2020\created\State2020HoverText.csv", "w", newline="") as hovertext:
    writer = csv.writer(hovertext)
    writer.writerow(header)
    for division in HoverText:
        writer.writerow([division, HoverText[division]])

