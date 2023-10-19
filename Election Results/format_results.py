from create_winner import createWinner
from create_first_pref import createFirstPref
from create_hover_text import createHoverText
from create_pref_flow import createPrefFlow


if __name__ == "__main__":
    createWinner("Council", "2020")
    createWinner("State", "2020")
    createWinner("Federal", "2022")

    createFirstPref("Council", "2020")
    createFirstPref("State", "2020")
    createFirstPref("Federal", "2022")

    createPrefFlow("Council", "2020")
    createPrefFlow("Federal", "2022")
    createPrefFlow("State", "2020")

    createHoverText("Council", "2020")
    createHoverText("State", "2020")
    createHoverText("Federal", "2022")

