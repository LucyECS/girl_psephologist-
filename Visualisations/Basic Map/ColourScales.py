def COLOURSCALE() -> dict:
    """
    Returns a dictionary of color codes for various political parties and other colors.

    Returns:
    dict: A dictionary with keys representing political parties and other colors, and values representing their corresponding color codes.
    """

    LABOR = '#E2363E'
    GREENS = '#009b40'
    LIBERALS = '#2279f1'
    INDEPENDENT = '#808080'

    # Set up the colourscales
    colourscales = {
        "Australian Labor Party": LABOR,
        "Liberal National Party of Queensland": LIBERALS,
        "Liberal": LIBERALS,
        "The Nationals": LIBERALS,
        "The Greens": GREENS,
        "Katter's Australian Party (KAP)": INDEPENDENT,
        "Independent": INDEPENDENT,
        "Centre Alliance": INDEPENDENT,
        "Government": LABOR,
        "Opposition": LIBERALS,
        "Cross Bench": INDEPENDENT,
        "GRN": GREENS,
        "ALP": LABOR,
        "LNP": LIBERALS,
        "IND": INDEPENDENT,
        "NP" : LIBERALS,
        "LP" : LIBERALS,
        "KAP": INDEPENDENT,
        "White": "#ffffff",
        "Black": "#000000",
        "Yellow": "#ffff00"
    }

    return colourscales
