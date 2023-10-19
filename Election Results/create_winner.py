# Import the required libraries
import xml.etree.ElementTree as ET
import csv

def createWinner(electionType: str, electionYear: str):

    if electionType == "Council" or electionType == "State":

        if electionType == "Council":
            if electionYear == "2020":
                fromFile = "Election Results\Council2020\Council2020publicResults.xml"
                toFile = "Election Results\Council2020\created\Council2020Winner.csv"
        if electionType == "State":
            if electionYear == "2020":
                fromFile = "Election Results\State2020\State2020publicResults.xml"
                toFile = "Election Results\State2020\created\State2020Winner.csv"

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
            if electionType == "Council":
                DivisionNmShort = (" ").join(DivisionNm.split(" ")[2:]).upper()
            elif electionType == "State":
                DivisionNmShort = DivisionNm.upper()
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

            # fix party name and abbreviation
            if PartyNm == None:
                PartyNm = "Independent"
                PartyAb = "IND"
            elif PartyNm == "Queensland Greens":
                PartyAb = "GRN"
            elif PartyNm == "Australian Labor Party (State of Queensland)":
                PartyAb = "ALP"
            elif PartyNm == "Pauline Hanson's One Nation Queensland Division":
                PartyAb = "ONP"


            
            data[DivisionNmShort] = [DivisionID, DivisionNmShort, GivenNm, Surname, PartyNm, PartyAb]
           

        # DivisionID,DivisionNm,StateAb,CandidateID,GivenNm,Surname,PartyNm,PartyAb
        WinnerHeader = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "PartyNm", "PartyAb"]


        # Write to Council2020Winner.csv
        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(WinnerHeader)
            for division in data:
                writer.writerow(data[division])


    if electionType == "Federal":
        # get the file names
        if electionYear == "2022":
            fromFile = "Election Results\Federal2022\HouseMembersElectedDownload-27966.csv"
            toFile = "Election Results\Federal2022\created\Federal2022Winner.csv"
        
        data = {}

        with open(fromFile) as raw_results:
            reader_obj = csv.DictReader(raw_results)

            # create rows
            rows = []
            for row in reader_obj:
                rows.append(row)

            for row in rows:
                DivisionID = row["DivisionID"]
                DivisionNm = row["DivisionNm"]
                GivenNm = row["GivenNm"]
                Surname = row["Surname"]
                PartyNm = row["PartyNm"]
                PartyAb = row["PartyAb"]
                data[DivisionNm] = [DivisionID, DivisionNm, GivenNm, Surname, PartyNm, PartyAb]

        # DivisionNm,GivenNm,Surname,PartyNm,PartyAb
        HEADER = ["DivisionID", "DivisionNm", "GivenNm", "Surname", "PartyNm", "PartyAb"]

        with open(toFile, "w", newline="") as results:
            writer = csv.writer(results)
            writer.writerow(HEADER)
            for division in data:
                writer.writerow(data[division])

if __name__ == "__main__":
    createWinner("Council", "2020")
    createWinner("State", "2020")
    createWinner("Federal", "2022")