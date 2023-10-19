from CreateWinner import createWinner
from CreateFirstPref import createFirstPref
from CreateHoverData import createHoverData
from CreatePrefFlow import createPrefFlow


if __name__ == "__main__":
    createWinner("Council", "2020")
    createWinner("State", "2020")
    createWinner("Federal", "2022")

    createFirstPref("Council", "2020")
    createFirstPref("State", "2020")
    createFirstPref("Federal", "2022")

    createPrefFlow("Federal", "2022")
    createPrefFlow("State", "2020")
    createPrefFlow("Council", "2020")


    createHoverData("Council", "2020")
    createHoverData("State", "2020")
    createHoverData("Federal", "2022")