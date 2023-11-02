def FILENAME() -> dict:
    """
    Returns a dictionary containing the file paths for various election results.

    Returns:
    filenames (dict): A dictionary containing the file paths for various election results.
    """
    filenames = {}

    filenames[("Council", "2020")] = {
        "winner" : "Election Results\Council2020\created\Council2020Winner.csv",
        "firstpref" : "Election Results\Council2020\created\Council2020FirstPref.csv",
        "prefflow" : "Election Results\Council2020\created\Council2020PrefFlow.csv",
        "hovertext" : "Election Results\Council2020\created\Council2020HoverText.csv",
        "boundaries" : "Boundaries\BCC.geojson",
        "featureidkey" : "properties.WARD"
    }

    filenames[("State", "2020")] = {
        "winner" : "Election Results\State2020\created\State2020Winner.csv",
        "firstpref" : "Election Results\State2020\created\State2020FirstPref.csv",
        "prefflow" : "Election Results\State2020\created\State2020PrefFlow.csv",
        "hovertext" : "Election Results\State2020\created\State2020HoverText.csv",
        "boundaries" : "Boundaries\State.geojson",
        "featureidkey" : "properties.NAME"
    }

    filenames[("Federal", "2022")] = {
        "winner" : "Election Results\Federal2022\created\Federal2022Winner.csv",
        "firstpref" : "Election Results\Federal2022\created\Federal2022FirstPref.csv",
        "prefflow" : "Election Results\Federal2022\created\Federal2022PrefFlow.csv",
        "hovertext" : "Election Results\Federal2022\created\Federal2022HoverText.csv",
        "boundaries" : "Boundaries\Federal.json",
        "featureidkey" : "properties.electorateName"
    }

    return filenames