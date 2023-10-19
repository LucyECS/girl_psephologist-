import csv

def createHoverData(electionType: str, electionYear: str):

    if electionType == "Council":
        if electionYear == "2020":
            fromFileFirstPref = "Election Results\Council2020\created\Council2020FirstPref.csv"
            fromFilePrefFlow = "Election Results\Council2020\created\Council2020PrefFlow.csv"
            toFile = "Election Results\Council2020\created\Council2020HoverText.csv"

    elif electionType == "State":
        if electionYear == "2020":
            fromFileFirstPref = "Election Results\State2020\created\State2020FirstPref.csv"
            fromFilePrefFlow = "Election Results\State2020\created\State2020PrefFlow.csv"
            toFile = "Election Results\State2020\created\State2020HoverText.csv"

    elif electionType == "Federal":
        if electionYear == "2022":
            fromFileFirstPref = "Election Results\Federal2022\created\Federal2022FirstPref.csv"
            fromFilePrefFlow = "Election Results\Federal2022\created\Federal2022PrefFlow.csv"
            toFile = "Election Results\Federal2022\created\Federal2022HoverText.csv"

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

    # READ FROM FIRST PREF CSV
    with open(fromFileFirstPref) as results:
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
            hovertext = "<br>" 
            hovertext = hovertext + "---------------------------------" + "<br>"

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
                        hovertext = hovertext + row["PartyAb"] + ": \t" + str(row["TotalVotes"]) + " (" + str(round(int(row["TotalVotes"])*100/(totalvotes), 2)) + "%" + ")" + "<br>"
            HoverText[division] = hovertext

    # READ FROM PREF FLOW CSV
    with open(fromFilePrefFlow) as results:
        # object to DictReader method 
        reader_obj = csv.DictReader(results)

        # CREATE ROWS
        rows = []
        for row in reader_obj:
            rows.append(row)

        # GET UNIQUE DIVISION NAMES
        DivisionNames = []
        for row in rows:
            if row["DivisionNm"] not in DivisionNames:
                DivisionNames.append(row["DivisionNm"])
        
        # GET DIVISION INFO (count number, ballot position, three candidate count number)
        DivsionInfo = {}
        for division in DivisionNames:
            ThreeCandidateCountNumber = None
            for row in rows:
                if row["DivisionNm"] == division:
                    if row["DistributingPartyAb"] in ["ALP", "LNP", "GRN"]:
                        if ThreeCandidateCountNumber == None:
                            ThreeCandidateCountNumber = str(int(row["CountNumber"])-1)
                    if ThreeCandidateCountNumber == None:
                        ThreeCandidateCountNumber = "0"
                    DivsionInfo[division] =[row["CountNumber"], row["BallotPosition"], ThreeCandidateCountNumber]

        for division in DivisionNames:
            hovertext = HoverText[division]

            hovertext = hovertext + "---------------------------------" + "<br>"
            hovertext = hovertext + "Three Party Prefered Numbers" + "<br>"
            
            totalCountNumber, totalBallotPosition, threeCandidateCountNumber = DivsionInfo[division]

            for row in rows:
                if row["DivisionNm"] == division:
                    # Give the 3PP votes
                    if row["CountNumber"] == threeCandidateCountNumber:
                        if row["PreferenceCount"] != "0":  # Removes candidates who have been eliminated
                            hovertext = hovertext + row["PartyAb"] + ": \t" + row["PreferenceCount"] + "(" + row["PreferencePercent"] + "%)" + "<br>"
                    
                    # Give the 3PP flows
                    if int(row["CountNumber"]) > int(threeCandidateCountNumber):
                        if row["PreferenceCount"] != "0": # Removes candidates who have been eliminated
                            pass
            HoverText[division] = hovertext

    # # print the hovertext of TENNYSON
    # text = HoverText["TENNYSON"]
    # # replace <br> with \n
    # text = text.replace("<br>", "\n")
    # print(text)
            



    # WRITE TO HOVER TEXT CSV
    with open(toFile, "w", newline="") as hovertext:
        writer = csv.writer(hovertext)
        writer.writerow(header)
        for division in HoverText:
            writer.writerow([division, HoverText[division]])

if __name__ == "__main__":
    createHoverData("Council", "2020")
    # createHoverData("State", "2020")
    # createHoverData("Federal", "2022")