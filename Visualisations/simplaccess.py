import csv

# import file names dictionary
from FILENAMES import FILENAME

# load in hover text file from the 2020 state election
with open(FILENAME()[("State", "2020")]["hovertext"], newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # create a dictionary of the hover text
    hover_text = {row['DivisionNm']: row['HoverPrefDetailed'] for row in reader}

# print hover text for a given division
text = hover_text['BULIMBA']
# replace the <br> tags with new lines
text = text.replace('<br>', '\n')
print(text)