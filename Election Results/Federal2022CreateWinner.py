import csv

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


