# Import the required libraries
import xml.etree.ElementTree as ET
import csv

def createWinner(election: str):

    if election == "Council2020":

        # Read the XML file
        tree = ET.parse('Election Results\BCC2020\Council2020publicResults.xml')
        root = tree.getroot()
        districts = root[2][8][1][0]

        data = {}

        for child in districts:
            DivisionID = child.get("number")
            DivisionNm = child.get("districtName")
            DivisionNmShort = (" ").join(DivisionNm.split(" ")[2:]).upper()
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
            data[DivisionNm] = [DivisionID, DivisionNmShort, GivenNm, Surname, PartyNm, PartyAb]

        # DivisionID,DivisionNm,StateAb,CandidateID,GivenNm,Surname,PartyNm,PartyAb
        WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "PartyNm", "PartyAb"]


        # Write to Council2020Winner.csv
        with open("Election Results\BCC2020\created\Council2020Winner.csv", "w", newline="") as winner:
            writer = csv.writer(winner)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])

    if election == "State2020":
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

    if election == "Federal2022":
        data = {}


        # read Election Results\Federal2022\HouseMembersElectedDownload-27966.csv
        with open("Election Results\Federal2022\HouseMembersElectedDownload-27966.csv") as results:
            # object to DictReader method 
            reader_obj = csv.DictReader(results)

            # create rows
            rows = []

            for row in reader_obj:
                rows.append(row)

            for row in rows:
                DivisionNm = row["DivisionNm"]
                GivenNm = row["GivenNm"]
                Surname = row["Surname"]
                PartyNm = row["PartyNm"]
                PartyAb = row["PartyAb"]
                data[DivisionNm] = [DivisionNm, GivenNm, Surname, PartyNm, PartyAb]

        # DivisionNm,GivenNm,Surname,PartyNm,PartyAb
        WinnerHeader = ["DivisionNm", "GivenNm", "Surname", "PartyNm", "PartyAb"]

        # Write to Federal2022Winner.csv
        with open("Election Results\Federal2022\created\Federal2022Winner.csv", "w", newline="") as winner:
            writer = csv.writer(winner)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])