import csv

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


