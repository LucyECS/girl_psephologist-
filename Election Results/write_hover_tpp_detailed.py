import csv

def writeHoverTPPDetailed(fromFileFirstPref: str, fromFilePrefFlow: str, electionType: str, end: str = "<br>"):
    gap = " "*5
    header = ["DivisionNm", "HoverText"]

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

    TotalVotesDict = {}

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
            hovertext = end 
            hovertext += "="*60 + end

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
            # Add dictionary entry for total votes
            TotalVotesDict[division] = totalvotes
            # Write division information to hovertext
            hovertext += gap*2 + "DIVISION INFORMATION" + end
            hovertext += "-"*60 + end
            hovertext += "Division Name: " + division + end
            hovertext += "Winner: " + winner + end
            hovertext += "Number of Candidates: " + str(numberofcandidates) + end
            hovertext += "Number of Formal Votes: " + '{:,}'.format(totalvotes) + end
            hovertext += "Number of Informal Votes: " + '{:,}'.format(informalvotes) + " (" + str(round(informalvotes*100/totalvotes, 2)) + "%" + ")" + end
            
            # PRIMARY VOTES
            hovertext += "="*60 + end
            hovertext += gap*2 + "PRIMARY VOTES" + end
            hovertext += "-"*60 + end
            # Iterate through each row to get primary votes and percentages and write to hovertext
            for row in rows:
                if row["DivisionNm"] == division:
                    if row["Surname"] != "Informal":
                        hovertext += row["PartyAb"] + ":" + gap + str(round(int(row["TotalVotes"])*100/(totalvotes), 2)) + "%" + gap + '{:,}'.format(int(row["TotalVotes"])) + end
            HoverText[division] = hovertext

    # READ FROM PREF FLOW CSV
    with open(fromFilePrefFlow) as results:
        # object to DictReader method 
        reader_obj = csv.DictReader(results)
        # create rows
        rows = []
        for row in reader_obj:
            rows.append(row)
        # get unique Division Names
        DIVISIONS = []
        for row in rows:
            if row["DivisionNm"] not in DIVISIONS:
                DIVISIONS.append(row["DivisionNm"])
        # Make a dictionary of the three party prefered count numbers
        ThreePPCount = {}
        # Make a dictionary of the margin between the bottom two candidates for each count
        BottomTwoMargin = {}
        for division in DIVISIONS:
            three_candidate_count_number = "-1"
            parties = []
            parties.append((0, ["", 0]))
            parties.append((1, ["", 1]))
            for row in rows:
                if row["DivisionNm"] == division:
                    # Getting first distribution where either ALP, LNP or GRN is distributed
                    if row["DistributingPartyAb"] in ["ALP", "LNP", "GRN"]:
                        if three_candidate_count_number == "-1":
                            three_candidate_count_number = str(int(row["CountNumber"])-1)
                    # Getting maxCountNumber and maxBallotNumber
                    if row["BallotPosition"] == "1":
                        parties.sort(reverse=False)
                        bottom_party = parties[0][1][0]
                        bottom_party_votes = parties[0][1][1]
                        next_bottom_party = parties[1][1][0]
                        next_bottom_party_votes = parties[1][1][1]

                        BottomTwoMargin[(division, row["CountNumber"])] = {"BottomParty": bottom_party, "BottomPartyVotes": bottom_party_votes, "NextBottomParty": next_bottom_party, "NextBottomPartyVotes": next_bottom_party_votes}
                        parties = []
                    if row["PartyNm"] != "Exhausted" and row["PreferenceCount"] != "0":
                        parties.append((int(row["PreferenceCount"]), [row["PartyAb"], int(row["PreferenceCount"])]))
            parties.sort(reverse=False)
            bottom_party = parties[0][1][0]
            bottom_party_votes = parties[0][1][1]
            next_bottom_party = parties[1][1][0]
            next_bottom_party_votes = parties[1][1][1]
            BottomTwoMargin = {(division, "Last"): {"BottomParty": bottom_party, "BottomPartyVotes": bottom_party_votes, "NextBottomParty": next_bottom_party, "NextBottomPartyVotes": next_bottom_party_votes}} | BottomTwoMargin
            ThreePPCount[division] = three_candidate_count_number

        for division in DIVISIONS:
            # INITIALISE HOVERTEXT
            hovertext = HoverText[division]
            flowtext = ""

            # THREE PARTY PREFERED NUMBERS
            hovertext += "="*60 + end
            hovertext += gap + "THREE PARTY PREFERED VOTES" + end
            hovertext += "-"*60 + end
            # iterate through each row
            for row in rows:
                if row["DivisionNm"] == division: # only rows for the division
                    if row["CountNumber"] == ThreePPCount[division]: # rows for the three candidate count
                        if row["PreferenceCount"] != "0":  # removes candidates who have been eliminated
                            if row["PartyNm"] != "Exhausted":
                                hovertext += row["PartyAb"] + ":" + gap + row["PreferencePercent"] + "%" + gap +'{:,}'.format(int(row["PreferenceCount"]))  + end
                            if row["PartyNm"] == "Exhausted" and electionType == "Council":
                                hovertext += "(Total Exhausted Percent: " + row["PreferencePercent"] + "%, Total Exhausted Count: " + '{:,}'.format(int(row["PreferenceCount"]))  + ")" + end

                    if int(row["CountNumber"]) == int(ThreePPCount[division])+1 and row["BallotPosition"] == "1":
                        hovertext += "="*60 + end
                        hovertext += gap*2 + "PREFERENCE FLOWS" + end

                    # Give the 3PP flows
                    if int(row["CountNumber"]) > int(ThreePPCount[division]) and row["BallotPosition"] == "1":
                        hovertext += flowtext
                        flowtext = ""
                        hovertext += "="*60 + end
                        margin = BottomTwoMargin[(division, row["CountNumber"])]
                        hovertext += "PREFERENCE FLOW FROM DISTRIBUTING: " + str(margin["BottomPartyVotes"]) + " " + row["DistributingPartyAb"] + end
                        hovertext += "(There was a margin of " + '{:,}'.format(int((margin["NextBottomPartyVotes"] - margin["BottomPartyVotes"])/2)) +  " (" + str(round((margin["NextBottomPartyVotes"] - margin["BottomPartyVotes"])*100/(2*TotalVotesDict[division]),2)) + "%)" + " votes between " + margin["BottomParty"] + " and " + margin["NextBottomParty"] + ")" + end
                        hovertext += "-"*60 + end
                        
                    if int(row["CountNumber"]) > int(ThreePPCount[division]): # rows after the three candidate count
                        if row["PreferenceCount"] != "0": # removes candidates who have been eliminated
                            if row["PartyNm"] != "Exhausted":
                                hovertext += row["DistributingPartyAb"] + " -> " + row["PartyAb"] + ":" + gap + row["TransferPercent"] + "%" + gap +'{:,}'.format(int(row["TransferCount"]))  + end
                                flowtext += row["PartyAb"] + ":" + gap + row["PreferencePercent"] + "%" + gap +'{:,}'.format(int(row["PreferenceCount"]))  + end
                            if row["PartyNm"] == "Exhausted" and electionType == "Council":
                                hovertext += row["DistributingPartyAb"] + " -> " + row["PartyAb"] + ":" + gap + row["TransferPercent"] + "%" + gap +'{:,}'.format(int(row["TransferCount"]))  + end
                                flowtext += "(Total Exhausted Percent: " + row["PreferencePercent"] + "%, Total Exhausted Count: " + '{:,}'.format(int(row["PreferenceCount"]))  + ")" + end
            hovertext += "-"*60 + end
            hovertext += flowtext
            margin = BottomTwoMargin[(division, "Last")]
            hovertext += "The winner is " + margin["NextBottomParty"] + " with a margin of " + '{:,}'.format(int((margin["NextBottomPartyVotes"] - margin["BottomPartyVotes"])/2)) +  " (" + str(round((margin["NextBottomPartyVotes"] - margin["BottomPartyVotes"])*100/(2*TotalVotesDict[division]),2)) + "%)" + " votes over " + margin["BottomParty"] + end
            HoverText[division] = hovertext

    return HoverText

if __name__ == "__main__":
    fromFileFirstPref = "Election Results\Council2020\created\Council2020FirstPref.csv"
    fromFilePrefFlow = "Election Results\Council2020\created\Council2020PrefFlow.csv"
    toFile = "Election Results\Council2020\created\Council2020HoverText.csv"

    HoverTPPDetailed = writeHoverTPPDetailed(fromFileFirstPref, fromFilePrefFlow, "Council")

    text = HoverTPPDetailed["PADDINGTON"]
    text = text.replace("<br>", "\n")
    print(text)