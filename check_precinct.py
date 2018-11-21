'''
Note: to run, you need to install shapely and shapefile
Also, change your path to wherever the precincts.shp file is
'''
from shapely.geometry import Polygon, Point, MultiPolygon
import shapefile 
import pandas as pd
import numpy as np

def getPrecinctData(filename):
    dataframe = pd.read_csv(filename)
    precincts = np.array(dataframe["Precinct"].tolist())
    crimeCounts = np.array(dataframe["Num Crimes"].tolist())
    
    # Dictionary that maps precinct number -> number of crimes
    precinctCrimeDict = dict(zip(dataframe["Precinct"], dataframe["Num Crimes"]))
    return precincts, crimeCounts, precinctCrimeDict

def main():

	path = 'C:\Users\Cassandra\Documents\precincts.shp'
	polygon = shapefile.Reader(path) 
	polygon = polygon.shapes() 

	precincts, crimeCounts, precinctCrimeDict = getPrecinctData('historic_crime.csv')


	shpfilePoints = [ shape.points for shape in polygon ]
	p_indices = range(34)

	#Dictionary that maps the index of the polygon to the corresponding precinct number
	indexToPrecinct = {}
	for i in range(len(precincts)):
		indexToPrecinct[i] = precincts[i]

	polygons = shpfilePoints
	point = Point(-73.986048, 40.762291)

	#Check if point is in the precinct
	#If it is, print out the precinct number 
	for i,polygon in enumerate(polygons):
	    poly = Polygon(polygon)
	    if poly.contains(point):
	    	print 'inside'
	    	precinct = indexToPrecinct.get(i)
	    	print "precinct number is ", precinct
	    	print "num crimes in precinct is ", precinctCrimeDict.get(precinct)


if __name__ == '__main__':
    main()