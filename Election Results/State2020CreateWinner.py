# Import the required libraries
import xml.etree.ElementTree as ET
import csv

# Read the XML file
tree = ET.parse('Election Results\State2020\State2020publicResults.xml')
root = tree.getroot()
districts = root[2][2]

data = {}

for child in districts:
    DivisionID = child.get("number")
    DivisionNm = child.get("districtName")
    for grandchild in child:


        # get declared candidates
        if grandchild.tag == "declaredCandidate":
            GivenNm = grandchild.get("ballotName").split(", ")[1]
            Surname = grandchild.get("ballotName").split(", ")[0]
            ballotPosition = grandchild.get("ballotOrderNumber")

        if grandchild.tag == "candidates":
            for greatgrandchild in grandchild:
                if greatgrandchild.get("ballotOrderNumber") == ballotPosition:
                    PartyNm = greatgrandchild.get("party")
                    PartyAb = greatgrandchild.get("partyCode")

    # add to data dictionary
    if PartyNm == None:
        PartyNm = "Independent"
        PartyAb = "IND"
    data[DivisionNm] = [DivisionID, DivisionNm, GivenNm, Surname, PartyNm, PartyAb]

# DivisionID,DivisionNm,StateAb,CandidateID,GivenNm,Surname,PartyNm,PartyAb
WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "PartyNm", "PartyAb"]


# Write to Council2020Winner.csv
with open("Election Results\State2020\created\State2020Winner.csv", "w", newline="") as winner:
    writer = csv.writer(winner)
    writer.writerow(WinnerHeader)
    for division in data:
        writer.writerow(data[division])

