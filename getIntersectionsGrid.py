import csv
import collections
import pandas as pd

# defaultDict for the grid
filename = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/nodeLocs.csv"


# Get all the data in the file
dataframe = pd.read_csv(filename, sep = ' ')
print (dataframe.head(5))


#TODO: get dict of all points and check if the found intersection is in the dict
def intersectionsToGrid():
	lats = dataframe["Latitude"].tolist()
	lons = dataframe["Longitude"].tolist()
	lats = sorted(lats)
	lons = sorted(lons)
	return lats, lons
