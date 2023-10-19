import csv
from write_hover_first_simple import writeHoverFirstSimple
from write_hover_tpp_simple import writeHoverTPPSimple
from write_hover_tpp_detailed import writeHoverTPPDetailed

def createHoverText(electionType: str, electionYear: str):
    if electionType == "Council":
        if electionYear == "2020":
            fromFileFirstPref = "Election Results\Council2020\created\Council2020FirstPref.csv"
            fromFilePrefFlow = "Election Results\Council2020\created\Council2020PrefFlow.csv"
            toFile = "Election Results\Council2020\created\Council2020HoverText.csv"

    elif electionType == "State":
        if electionYear == "2020":
            fromFileFirstPref = "Election Results\State2020\created\State2020FirstPref.csv"
            fromFilePrefFlow = "Election Results\State2020\created\State2020PrefFlow.csv"
            toFile = "Election Results\State2020\created\State2020HoverText.csv"

    elif electionType == "Federal":
        if electionYear == "2022":
            fromFileFirstPref = "Election Results\Federal2022\created\Federal2022FirstPref.csv"
            fromFilePrefFlow = "Election Results\Federal2022\created\Federal2022PrefFlow.csv"
            toFile = "Election Results\Federal2022\created\Federal2022HoverText.csv"

    header = ["DivisionNm", "HoverFirstSimple", "HoverTPPSimple", "HoverTPPDetailed"]

    HoverFirstSimple = writeHoverFirstSimple(fromFileFirstPref, fromFilePrefFlow, electionType)
    HoverTPPSimple = writeHoverTPPSimple(fromFileFirstPref, fromFilePrefFlow, electionType)
    HoverTPPDetailed = writeHoverTPPDetailed(fromFileFirstPref, fromFilePrefFlow, electionType)

    with open(toFile, "w", newline="") as results:
        writer = csv.writer(results)
        writer.writerow(header)
        for division in HoverFirstSimple:
            writer.writerow([division, HoverFirstSimple[division], HoverTPPSimple[division], HoverTPPDetailed[division]])

if __name__ == "__main__":
    createHoverText("Council", "2020")
    createHoverText("State", "2020")
    createHoverText("Federal", "2022")