import json

def Centre_BCC() -> dict:
    """
    Returns a dictionary of the center coordinates of each ward in Brisbane City Council
    """

    centers = {}

    with open('Boundaries\BCC.geojson') as f:
        data = json.load(f)

    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            center = [sum([c[0] for c in coordinates[0]])/len(coordinates[0]), sum([c[1] for c in coordinates[0]])/len(coordinates[0])]
        elif feature['geometry']['type'] == 'MultiPolygon':
            center = []
            for polygon in coordinates:
                center.append([sum([c[0] for c in polygon[0]])/len(polygon[0]), sum([c[1] for c in polygon[0]])/len(polygon[0])])
        ward_name = feature['properties']['WARD']
        centers[ward_name] = center

    return centers

def Centre_State() -> dict:
    """
    Returns a dictionary of the center coordinates of each electorate in the state level
    """

    centers = {}

    with open('Boundaries\State.geojson') as f:
        data = json.load(f)

    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            center = [sum([c[0] for c in coordinates[0]])/len(coordinates[0]), sum([c[1] for c in coordinates[0]])/len(coordinates[0])]
        elif feature['geometry']['type'] == 'MultiPolygon':
            center = []
            for polygon in coordinates:
                center.append([sum([c[0] for c in polygon[0]])/len(polygon[0]), sum([c[1] for c in polygon[0]])/len(polygon[0])])
        electorate_name = feature['properties']['NAME']
        centers[electorate_name] = center

    return centers

def Centre_Federal() -> dict:
    """
    Returns a dictionary of the center coordinates of each electorate in the federal level
    """

    centers = {}

    with open('Boundaries\Federal.json') as f:
        data = json.load(f)

    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            center = [[sum([c[0] for c in coordinates[0]])/len(coordinates[0]), sum([c[1] for c in coordinates[0]])/len(coordinates[0])]]
        elif feature['geometry']['type'] == 'MultiPolygon':
            center = []
            for polygon in coordinates:
                center.append([sum([c[0] for c in polygon[0]])/len(polygon[0]), sum([c[1] for c in polygon[0]])/len(polygon[0])])
        electorate_name = feature['properties']['electorateName']
        centers[electorate_name] = center

    return centers

def CENTRES() -> dict:
    centres = {}
    centres['State'] = Centre_State()
    centres['Council'] = Centre_BCC()
    centres['Federal'] = Centre_Federal()

    return centres

if __name__ == "__main__":
    # print(Centre_BCC())
    # print(Centre_State())
    # print(Centre_Federal())

    centres = Centre_Federal()
    for ward in centres:
        print(ward, centres[ward])