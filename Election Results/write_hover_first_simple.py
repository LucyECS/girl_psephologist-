import csv

def writeHoverFirstSimple(fromFileFirstPref: str, fromFilePrefFlow: str, electionType: str) -> dict:
    #  Example Hover Text
    """
    ============================================================
    Division Information
    ------------------------------------------------------------
    Division Name: TENNYSON
    Winner: Independent (Nicole, JOHNSTON)
    Number of Candidates: 5
    Number of Formal Votes: 23,046
    Number of Informal Votes: 383 (1.66%)
    ============================================================
    Primary Votes
    ------------------------------------------------------------
    LNP:    19.07%          4,394
    GRN:    13.27%          3,058
    ALP:    13.94%          3,212
    IND:    50.21%          11,571
    AJP:    1.86%           428
    ============================================================
    Three Party Prefered Numbers
    ------------------------------------------------------------
    LNP:    19.71%          4,421
    GRN:    14.02%          3,146
    ALP:    14.45%          3,241
    IND:    51.82%          11,624
    """

    HoverText = {}

    # READ FROM FIRST PREF CSV
    with open(fromFileFirstPref) as results:
        # object to DictReader method 
        reader_obj = csv.DictReader(results)

        # create rows
        rows = []
        for row in reader_obj:
            rows.append(row)

        # Get unique Division Names
        DIVISIONS = []
        for row in rows:
            if row["DivisionNm"] not in DIVISIONS:
                DIVISIONS.append(row["DivisionNm"])

        # Iterate through each Division
        for division in DIVISIONS:

            # INITIALISE HOVERTEXT
            hovertext = "<br>" 
            hovertext += "="*60 + "<br>"

            # DIVISION INFORMATION
            totalvotes = 0
            informalvotes = 0
            numberofcandidates = -1
            winner = ""
            # Iterate through each row to get division information
            for row in rows:
                if row["DivisionNm"] == division:
                    totalvotes = totalvotes + int(row["TotalVotes"])
                    numberofcandidates = numberofcandidates + 1
                    if row["Surname"] == "Informal":
                        informalvotes = informalvotes + int(row["TotalVotes"])
                    if row["Elected"] == "Y":
                        winner = row["PartyNm"] + " (" + row["GivenNm"] + ", " + row["Surname"] + ")"
            # Write division information to hovertext
            hovertext += "Division Information" + "<br>"
            hovertext += "-"*60 + "<br>"
            hovertext += "Division Name: " + division + "<br>"
            hovertext += "Winner: " + winner + "<br>"
            hovertext += "Number of Candidates: " + str(numberofcandidates) + "<br>"
            hovertext += "Number of Formal Votes: " + '{:,}'.format(totalvotes) + "<br>"
            hovertext += "Number of Informal Votes: " + '{:,}'.format(informalvotes) + " (" + str(round(informalvotes*100/totalvotes, 2)) + "%" + ")" + "<br>"
            
            # PRIMARY VOTES
            hovertext += "="*60 + "<br>"
            hovertext += "Primary Votes" + "<br>"
            hovertext += "-"*60 + "<br>"
            # Iterate through each row to get primary votes and percentages and write to hovertext
            for row in rows:
                if row["DivisionNm"] == division:
                    if row["Surname"] != "Informal":
                        hovertext += row["PartyAb"] + ": \t\t  " + str(round(int(row["TotalVotes"])*100/(totalvotes), 2)) + "%\t\t\t\t    " + '{:,}'.format(int(row["TotalVotes"])) + "<br>"
            HoverText[division] = hovertext

    return HoverText
    

if __name__ == "__main__":
    fromFileFirstPref = "Election Results\Council2020\created\Council2020FirstPref.csv"
    fromFilePrefFlow = "Election Results\Council2020\created\Council2020PrefFlow.csv"
    toFile = "Election Results\Council2020\created\Council2020HoverText.csv"

    HoverTPPSimple = writeHoverFirstSimple(fromFileFirstPref, fromFilePrefFlow, "Council")

    text = HoverTPPSimple["TENNYSON"]
    text = text.replace("<br>", "\n")
    print(text)