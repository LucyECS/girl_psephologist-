# Import the required libraries
import xml.etree.ElementTree as ET
import csv

def createFirstPref(electionType: str, electionYear: str):
    if electionType == "Council" or electionType == "State":

        if electionType == "Council":
            if electionYear == "2020":
                fromFile = "Election Results\Council2020\Council2020publicResults.xml"
                toFile = "Election Results\Council2020\created\Council2020FirstPref.csv"
        if electionType == "State":
            if electionYear == "2020":
                fromFile = "Election Results\State2020\State2020publicResults.xml"
                toFile = "Election Results\State2020\created\State2020FirstPref.csv"

        # Read the XML file
        tree = ET.parse(fromFile)
        root = tree.getroot()

        if electionType == "Council" and electionYear == "2020":
            districts = root[2][8][1][0]
        elif electionType == "State" and electionYear == "2020":
            districts = root[2][2]

        data = {}

        # make dictionary of partys
        partys = {}

        for child in districts:
            DivisionID = child.get("number")
            DivisionNm = child.get("districtName")
            if electionType == "Council":
                DivisionNmShort = (" ").join(DivisionNm.split(" ")[2:]).upper()
            elif electionType == "State":
                DivisionNmShort = DivisionNm.upper()
            for grandchild in child:


                # get declared candidates
                if grandchild.tag == "declaredCandidate":
                    winnerBallotPosition = grandchild.get("ballotOrderNumber")

                
                if grandchild.tag == "candidates":
                    for greatgrandchild in grandchild:
                        partys[greatgrandchild.get("ballotName")] = [greatgrandchild.get("party"), greatgrandchild.get("partyCode")]


                # count round Official First Preference Count
                if grandchild.get("countName") == "Official First Preference Count":
                    for greatgrandchild in grandchild:

                        if greatgrandchild.tag == "totalInformalVotes":
                            GivenNm = "Informal"
                            Surname = "Informal"
                            PartyNm = "Informal"
                            PartyAb = "INF"
                            Elected = "N"
                            BallotPosition = "0"
                            totalVotes = greatgrandchild[0].text
                            data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNmShort, GivenNm, Surname, BallotPosition, Elected, PartyAb, PartyNm, totalVotes]

                        if greatgrandchild.tag == "primaryVoteResults":
                            for greatgreatgrandchild in greatgrandchild:
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

                                # fix party name and abbreviation
                                if PartyNm == None or PartyAb == None:
                                    PartyNm = "Independent"
                                    PartyAb = "IND"
                                elif PartyNm == "Queensland Greens":
                                    PartyAb = "GRN"
                                elif PartyNm == "Australian Labor Party (State of Queensland)":
                                    PartyAb = "ALP"
                                elif PartyNm == "Pauline Hanson's One Nation Queensland Division":
                                    PartyAb = "ONP"
                                elif PartyNm == "Clive Palmer's United Australia Party":
                                    PartyAb = "UAP"
                                elif PartyNm == "Motorists Party":
                                    PartyAb = "MP"
                                elif PartyNm == "Animal Justice Party (Queensland)":
                                    PartyAb = "AJP"


                                data[(DivisionNm, BallotPosition)] = [DivisionID, DivisionNmShort, GivenNm, Surname, BallotPosition, Elected, PartyAb, PartyNm, totalVotes]
                                
                                    

        # StateAb,DivisionID,DivisionNm,CandidateID,Surname,GivenNm,BallotPosition,Elected,HistoricElected,PartyAb,PartyNm,OrdinaryVotes,AbsentVotes,ProvisionalVotes,PrePollVotes,PostalVotes,TotalVotes,Swing
        HEADER = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "BallotPosition", "Elected", "PartyAb", "PartyNm", "TotalVotes"]

        # Write to Council2020FirstPref.csv
        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(HEADER)
            for division in data:
                writer.writerow(data[division])


    if electionType == "Federal":
        if electionYear == "2022":
            fromFile = "Election Results/Federal2022/HouseFirstPrefsByCandidateByVoteTypeDownload-27966.csv"
            toFile = "Election Results\Federal2022\created\Federal2022FirstPref.csv"

        data = {}


        # read Election Results\Federal2022\HouseMembersElectedDownload-27966.csv
        with open(fromFile) as results:
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
                if PartyNm == "" or PartyAb == "":
                    PartyNm = "Independent"
                    PartyAb == "IND"
                data[(DivisionNm, Surname)] = [DivisionID, DivisionNm, GivenNm, Surname, BallotPosition, Elected, PartyNm, PartyAb, TotalVotes]

        # DivisionID,DivisionNm,GivenNm,Surname,BallotPosition,Elected,PartyAb,PartyNm,TotalVotes
        HEADER = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "BallotPosition", "Elected", "PartyNm", "PartyAb", "TotalVotes"]

        # Write to Federal2022Winner.csv
        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(HEADER)
            for division in data:
                writer.writerow(data[division])


if __name__ == "__main__":
    createFirstPref("Council", "2020")
    createFirstPref("State", "2020")
    createFirstPref("Federal", "2022")