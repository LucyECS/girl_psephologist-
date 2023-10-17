# Import the required libraries
import xml.etree.ElementTree as ET
import csv

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




