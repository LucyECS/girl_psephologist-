# Import the required libraries
import xml.etree.ElementTree as ET
import csv


def createPrefFlow(electionType: str, electionYear: str):
    """
    Reads the election results from a CSV file and creates a new CSV file with preference flow data.

    Args:
        electionType (str): The type of election (e.g. "Federal").
        electionYear (str): The year of the election (e.g. "2022").

    Returns:
        None
    """

    if electionType == "Federal":

        if electionYear == "2022":
            fromFile = "Election Results\Federal2022\HouseDopByDivisionDownload-27966.csv"
            toFile = "Election Results\Federal2022\created\Federal2022PrefFlow.csv"

        data = {}
        with open(fromFile) as raw_results:
            # object to DictReader method 
            reader_obj = csv.DictReader(raw_results)

            # create rows
            rows = []
            for row in reader_obj:
                if row["PartyAb"] == "":
                    row["PartyAb"] = "IND"
                    row["PartyNm"] = "Independent"
                rows.append(row)

            # create dictionary of divisions with number of counts and ballot positions
            divisions = {}
            for row in rows:
                divisions[row["DivisionNm"]] = (row["CountNumber"], row["BallotPosition"])

            # collect PreferenceCount, PreferencePercent, TransferCount, TransferPercent, Winner, distributing
            prefenceCount = {}
            prefencePercent = {}
            transferCount = {}
            transferPercent = {}
            winner = {}
            distributing = {}
            for row in rows:
                if row["CalculationType"] == "Preference Count":
                    prefenceCount[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])] = row["CalculationValue"]
                elif row["CalculationType"] == "Preference Percent":
                    prefencePercent[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])] = row["CalculationValue"]
                elif row["CalculationType"] == "Transfer Count":
                    transferCount[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])] = row["CalculationValue"]
                elif row["CalculationType"] == "Transfer Percent":
                    transferPercent[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])] = row["CalculationValue"]
                if row["Elected"] == "Y":
                    winner[row["DivisionNm"]] = row["PartyAb"]
                if row["CalculationType"] == "Transfer Percent" and row["CalculationValue"] == "-100":
                    distributing[(row["DivisionNm"], row["CountNumber"])] = [row["BallotPosition"], row["Surname"], row["GivenNm"], row["PartyAb"], row["PartyNm"]]
            
            # DivisionNm, CountNumber, BallotPosition
            previous = [None, None, None]
            current = [rows[0]["DivisionNm"], rows[0]["CountNumber"], rows[0]["BallotPosition"]]
            # add to data dictionary
            for row in rows:
                if (row["DivisionNm"], row["CountNumber"]) in distributing:
                    distributing_info = distributing[(row["DivisionNm"], row["CountNumber"])]
                else:
                    distributing_info = ["First Pref"]*5


                previous = current
                current = [row["DivisionNm"], row["CountNumber"], row["BallotPosition"]] + distributing_info


                # create the exhaustive count
                if previous[1] != current[1]:
                    ballotPosition = str(int(previous[2])+1)
                    data[(previous[0], previous[1], ballotPosition)] = [previous[0], previous[1], ballotPosition, "Exhausted", "Exhausted", "Exhuasted", "Exhausted", "N", 0, 0, 0, 0, winner[previous[0]]] + previous[3:]
                
                
                # create the row_informantion
                info = [row["DivisionNm"], row["CountNumber"], row["BallotPosition"], row["Surname"], row["GivenNm"], row["PartyAb"], row["PartyNm"], row["Elected"],
                         prefenceCount[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])],
                           prefencePercent[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])],
                             transferCount[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])],
                               transferPercent[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])],
                                 winner[row["DivisionNm"]]] 
                info += current[3:]
                data[(row["DivisionNm"], row["CountNumber"], row["BallotPosition"])] = info


        # DivisionNm,CountNumber,BallotPosition,Surname,GivenNm,PartyAb,PartyNm,Elected,PreferenceCount, PreferencePercent, TransferCount, TransferPercent, ExhausedCount, ExhausedPercent
        HEADER = ["DivisionNm", "CountNumber", "BallotPosition", "Surname", "GivenNm", "PartyAb", "PartyNm", "Elected", "PreferenceCount", "PreferencePercent", "TransferCount", "TransferPercent", "Winner", "DistributingBallotPosition", "DistributingSurname", "DistributingGivenNm", "DistributingPartyAb", "DistributingPartyNm"]

        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(HEADER)
            for line in data.values():
                writer.writerow(line)

    elif electionType == "State" or electionType == "Council":
        if electionType == "Council":
            if electionYear == "2020":
                fromFile = "Election Results\Council2020\Council2020publicResults.xml"
                toFile = "Election Results\Council2020\created\Council2020PrefFlow.csv"
        if electionType == "State":
            if electionYear == "2020":
                fromFile = "Election Results\State2020\State2020publicResults.xml"
                toFile = "Election Results\State2020\created\State2020FPrefFlow.csv"

        # Read the XML file
        tree = ET.parse(fromFile)
        root = tree.getroot()

        if electionType == "Council" and electionYear == "2020":
            districts = root[2][8][1][0]
        elif electionType == "State" and electionYear == "2020":
            districts = root[2][2]

        data = {}

        for child in districts:
            DivisionID = child.get("number")
            DivisionNm = child.get("districtName")
            print(DivisionNm)
            if electionType == "Council":
                DivisionNmShort = (" ").join(DivisionNm.split(" ")[2:]).upper()
            elif electionType == "State":
                DivisionNmShort = DivisionNm.upper()

            candidates = {}
            for grandchild in child:

                # get declared candidates
                if grandchild.tag == "declaredCandidate":
                    winnerBallotPosition = grandchild.get("ballotOrderNumber")

                if grandchild.tag == "candidates":
                    for greatgrandchild in grandchild:
                        # get candidate info
                        ballotName = greatgrandchild.get("ballotName")
                        Surname = ballotName.split(", ")[0]
                        GivenNm = ballotName.split(", ")[1]
                        ballotPosition = greatgrandchild.get("ballotOrderNumber")
                        party = greatgrandchild.get("party")
                        partyCode = greatgrandchild.get("partyCode")

                        # fix partyCode
                        if partyCode == "Australian Labor Party":
                            partyCode = "ALP"
                        if partyCode == "Clive Palmer's UAP":
                            partyCode = "UAP"
                        if partyCode == "Pauline Hanson's One Nation":
                            partyCode = "ONP"

                        # get if elected
                        if ballotPosition == winnerBallotPosition:
                            Elected = "Y"
                            Winner = partyCode
                        else:
                            Elected = "N"

                        # add to dictionary of candidates
                        candidates[ballotPosition] = [ballotPosition, Surname, GivenNm, partyCode, party, Elected]

                



                        

                # count round Official Distribution of Preference Count
                if grandchild.get("countName") == "Official Distribution of Preferences Count":

                    for greatgrandchild in grandchild:
                        if greatgrandchild.tag == "preferenceDistributionSummary":
                            for distribution in greatgrandchild:

                                if distribution.tag == "primaryVotes":
                                    CountNumber = 0
                                    for candidate in distribution:
                                        ballotOrderNumber = candidate.get("ballotOrderNumber")

                                        # candidate info
                                        ballotPosition, Surname, GivenNm, partyCode, party, Elected = candidates[ballotOrderNumber]

                                        PreferenceCount = candidate[0].text
                                        PreferencePercent = candidate[1].text

                                        # add to data dictionary
                                        data[(DivisionNmShort, str(CountNumber), ballotPosition)] = [DivisionNm, CountNumber, ballotPosition, Surname, GivenNm, partyCode, party, Elected, 
                                                                                                PreferenceCount, PreferencePercent, 0, 0, Winner, 
                                                                                                "First Pref", "First Pref", "First Pref", "First Pref", "First Pref"]
                                
                                    # add exhausted
                                    ballotPosition = str(int(ballotPosition)+1)
                                    data[(DivisionNmShort, str(CountNumber), ballotPosition)] = [DivisionNm, CountNumber, ballotPosition, "Exhausted", "Exhausted", "Exhausted", "Exhausted", "N", 
                                                                                            0, 0, 0, 0, Winner, "First Pref", "First Pref", "First Pref", "First Pref", "First Pref"]
                                
                                
                                # get the distribution of preferences
                                elif distribution.tag == "preferenceDistribution":
                                    CountNumber = distribution.get("distribution")

                                    DistributingBallotPosition, DistributingSurname, DistributingGivenNm, DistributingPartyAb, DistributingPartyNm, DistributingExcluded = candidates[distribution.get("excludedBallotOrder")]
                                    
                                    if electionType == "Council":
                                        exhaustedCount = distribution.find("exhausted")[0].text
                                        exhaustedPercent = distribution.find("exhausted")[1].text

                                    elif electionType == "State":
                                        exhaustedCount = "0"
                                        exhaustedPercent = "0"
                                    
                                    
                                    # write for each candidate
                                    for candidate in candidates:

                                        # candidate info
                                        ballotPosition, Surname, GivenNm, partyCode, party, Elected = candidates[candidate]
                                        PreferenceCount, PreferencePercent, TransferCount, TransferPercent = 0,0,0,0

                                        # counts for distributing candidate
                                        if candidate == DistributingBallotPosition:
                                            TransferCount = str(-int(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][8]))
                                            TransferPercent = str(-float(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][9]))
                                            PreferenceCount = "0"
                                            PreferencePercent = "0"

                                        for possible_candiate in distribution:
                                            if possible_candiate.get("ballotOrderNumber") == candidate:
                                                transferCount = possible_candiate[0].text
                                                transferPercent = possible_candiate[1].text

                                                PreferenceCount = str(int(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][8]) + int(TransferCount))
                                                PreferencePercent = str(float(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][9]) + float(TransferPercent))

                                        data[(DivisionNmShort, CountNumber, ballotPosition)] = [DivisionNm, CountNumber, ballotPosition, Surname, GivenNm, partyCode, party, Elected,
                                                                                                    PreferenceCount, PreferencePercent, transferCount, transferPercent, Winner, 
                                                                                                    DistributingBallotPosition, DistributingSurname, DistributingGivenNm, DistributingPartyAb, DistributingPartyNm]

                                    # write for exhausted
                                    TransferCount = exhaustedCount
                                    TransferPercent = exhaustedPercent
                                    
                                    PreferenceCount = int(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][8]) + int(TransferCount)
                                    PreferencePercent = float(data[(DivisionNmShort, str(int(CountNumber)-1), ballotPosition)][9]) + float(TransferPercent)
                                    
                                    ballotPosition = str(int(ballotPosition)+1)
                                    data[(DivisionNmShort, CountNumber, ballotPosition)] = [DivisionNm, CountNumber, ballotPosition, "Exhausted", "Exhausted", "Exhausted", "Exhausted", "N",
                                                                                                0, 0, 0, 0, Winner, DistributingBallotPosition, DistributingSurname, DistributingGivenNm, DistributingPartyAb, DistributingPartyNm]
                                
                                

        # StateAb,DivisionID,DivisionNm,CandidateID,Surname,GivenNm,BallotPosition,Elected,HistoricElected,PartyAb,PartyNm,OrdinaryVotes,AbsentVotes,ProvisionalVotes,PrePollVotes,PostalVotes,TotalVotes,Swing
        HEADER = ["DivisionNm", "CountNumber", "BallotPosition", "Surname", "GivenNm", "PartyAb", "PartyNm", "Elected", 
                  "PreferenceCount", "PreferencePercent", "TransferCount", "TransferPercent", "Winner", "DistributingBallotPosition", "DistributingSurname", "DistributingGivenNm", "DistributingPartyAb", "DistributingPartyNm"]

        # Write to Council2020FirstPref.csv
        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(HEADER)
            for division in data:
                writer.writerow(data[division])


    
                

if __name__ == "__main__":
    # createPrefFlow("Federal", "2022")
    createPrefFlow("Council", "2020")
    # createPrefFlow("State", "2020")