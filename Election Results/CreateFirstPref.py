# Import the required libraries
import xml.etree.ElementTree as ET
import csv

def createFirstPref(election: str):
    if election == "Council2020":

        # Read the XML file
        tree = ET.parse("Election Results\BCC2020\Council2020publicResults.xml")
        root = tree.getroot()
        districts = root[2][8][1][0]

        data = {}

        # make dictionary of partys
        partys = {}

        for child in districts:
            DivisionID = child.get("number")
            DivisionNm = child.get("districtName")
            DivisionNmShort = (" ").join(DivisionNm.split(" ")[2:]).upper()
            print(child.tag, child.attrib)
            for grandchild in child:
                print("\t", grandchild.tag, grandchild.attrib)


                # get declared candidates
                if grandchild.tag == "declaredCandidate":
                    winnerBallotPosition = grandchild.get("ballotOrderNumber")

                
                if grandchild.tag == "candidates":
                    for greatgrandchild in grandchild:
                        print("\t\t", greatgrandchild.tag, greatgrandchild.attrib)
                        partys[greatgrandchild.get("ballotName")] = [greatgrandchild.get("party"), greatgrandchild.get("partyCode")]


                # count round Official First Preference Count
                if grandchild.get("countName") == "Official First Preference Count":
                    for greatgrandchild in grandchild:
                        print("\t\t", greatgrandchild.tag, greatgrandchild.attrib)

                        if greatgrandchild.tag == "totalInformalVotes":
                            GivenNm = "Informal"
                            Surname = "Informal"
                            PartyNm = "Informal"
                            PartyAb = "Informal"
                            Elected = "N"
                            BallotPosition = "0"
                            totalVotes = greatgrandchild[0].text
                            print(totalVotes)
                            data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNmShort, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, totalVotes]

                        if greatgrandchild.tag == "primaryVoteResults":
                            for greatgreatgrandchild in greatgrandchild:
                                print("\t\t\t", greatgreatgrandchild.tag, greatgreatgrandchild.attrib)
                                GivenNm = greatgreatgrandchild.get("ballotName").split(", ")[1]
                                Surname = greatgreatgrandchild.get("ballotName").split(", ")[0]
                                PartyNm = partys[greatgreatgrandchild.get("ballotName")][0]
                                PartyAb = partys[greatgreatgrandchild.get("ballotName")][1]
                                BallotPosition = greatgreatgrandchild.get("ballotOrderNumber")
                                if BallotPosition == winnerBallotPosition:
                                    Elected = "Y"
                                else:
                                    Elected = "N"
                                totalVotes = greatgreatgrandchild[0].text

                                if PartyNm == None:
                                    PartyNm = "Independent"
                                    PartyAb = "IND"
                                data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNmShort, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, totalVotes]
                                    

        # StateAb,DivisionID,DivisionNm,CandidateID,Surname,GivenNm,BallotPosition,Elected,HistoricElected,PartyAb,PartyNm,OrdinaryVotes,AbsentVotes,ProvisionalVotes,PrePollVotes,PostalVotes,TotalVotes,Swing
        WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "BallotPosition", "Elected", "PartyAb", "PartyNm", "TotalVotes"]

        # Write to Council2020FirstPref.csv
        with open("Election Results\BCC2020\created\Council2020FirstPref.csv", "w", newline="") as winner:
            writer = csv.writer(winner)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])

    if election == "State2020":
        # Read the XML file
        tree = ET.parse("Election Results\State2020\State2020publicResults.xml")
        root = tree.getroot()
        districts = root[2][2]

        data = {}

        # make dictionary of partys
        partys = {}

        for child in districts:
            DivisionID = child.get("number")
            DivisionNm = child.get("districtName")
            print(child.tag, child.attrib)
            for grandchild in child:
                print("\t", grandchild.tag, grandchild.attrib)


                # get declared candidates
                if grandchild.tag == "declaredCandidate":
                    winnerBallotPosition = grandchild.get("ballotOrderNumber")

                
                if grandchild.tag == "candidates":
                    for greatgrandchild in grandchild:
                        print("\t\t", greatgrandchild.tag, greatgrandchild.attrib)
                        partys[greatgrandchild.get("ballotName")] = [greatgrandchild.get("party"), greatgrandchild.get("partyCode")]


                # count round Official First Preference Count
                if grandchild.get("countName") == "Official First Preference Count":
                    for greatgrandchild in grandchild:
                        print("\t\t", greatgrandchild.tag, greatgrandchild.attrib)

                        if greatgrandchild.tag == "totalInformalVotes":
                            GivenNm = "Informal"
                            Surname = "Informal"
                            PartyNm = "Informal"
                            PartyAb = "Informal"
                            Elected = "N"
                            BallotPosition = "0"
                            totalVotes = greatgrandchild[0].text
                            print(totalVotes)
                            data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNm, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, totalVotes]

                        if greatgrandchild.tag == "primaryVoteResults":
                            for greatgreatgrandchild in greatgrandchild:
                                print("\t\t\t", greatgreatgrandchild.tag, greatgreatgrandchild.attrib)
                                GivenNm = greatgreatgrandchild.get("ballotName").split(", ")[1]
                                Surname = greatgreatgrandchild.get("ballotName").split(", ")[0]
                                PartyNm = partys[greatgreatgrandchild.get("ballotName")][0]
                                PartyAb = partys[greatgreatgrandchild.get("ballotName")][1]
                                BallotPosition = greatgreatgrandchild.get("ballotOrderNumber")
                                if BallotPosition == winnerBallotPosition:
                                    Elected = "Y"
                                else:
                                    Elected = "N"
                                totalVotes = greatgreatgrandchild[0].text

                                if PartyNm == None:
                                    PartyNm = "Independent"
                                    PartyAb = "IND"
                                data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNm, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, totalVotes]
                                    

        # StateAb,DivisionID,DivisionNm,CandidateID,Surname,GivenNm,BallotPosition,Elected,HistoricElected,PartyAb,PartyNm,OrdinaryVotes,AbsentVotes,ProvisionalVotes,PrePollVotes,PostalVotes,TotalVotes,Swing
        WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "BallotPosition", "Elected", "PartyAb", "PartyNm", "TotalVotes"]

        # Write to Council2020FirstPref.csv
        with open("Election Results\State2020\created\State2020FirstPref.csv", "w", newline="") as winner:
            writer = csv.writer(winner)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])

    if election == "Federal2022":
        data = {}


        # read Election Results\Federal2022\HouseMembersElectedDownload-27966.csv
        with open("Election Results\Federal2022\HouseFirstPrefsByCandidateByVoteTypeDownload-27966.csv") as results:
            # object to DictReader method 
            reader_obj = csv.DictReader(results)

            # create rows
            rows = []

            for row in reader_obj:
                rows.append(row)

            for row in rows:
                DivisionID = row["DivisionID"]
                DivisionNm = row["DivisionNm"]
                GivenNm = row["GivenNm"]
                Surname = row["Surname"]
                BallotPosition = row["BallotPosition"]
                Elected = row["Elected"]
                PartyNm = row["PartyNm"]
                PartyAb = row["PartyAb"]
                TotalVotes = row["TotalVotes"]
                data[(DivisionNm, Surname)] = [DivisionID, DivisionNm, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, TotalVotes]

        # DivisionID,DivisionNm,GivenNm,Surname,BallotPosition,Elected,PartyAb,PartyNm,TotalVotes
        WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "BallotPosition", "Elected", "PartyNm", "PartyAb", "TotalVotes"]

        # Write to Federal2022Winner.csv
        with open("Election Results\Federal2022\created\Federal2022FirstPref.csv", "w", newline="") as winner:
            writer = csv.writer(winner)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])


