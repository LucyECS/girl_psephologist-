from CreateWinner import createWinner
from CreateFirstPref import createFirstPref
from CreateHoverData import createHoverData


if __name__ == "__main__":
    createWinner("Council2020")
    createWinner("State2020")
    createWinner("Federal2022")
    createFirstPref("Council2020")
    createFirstPref("State2020")
    createFirstPref("Federal2022")
    createHoverData("Council2020")
    createHoverData("State2020")
    createHoverData("Federal2022")

