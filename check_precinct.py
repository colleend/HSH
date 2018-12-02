'''
Note: to run, you need to install shapely and shapefile
Also, change your path to wherever the precincts.shp file is
'''
from shapely.geometry import Polygon, Point, MultiPolygon
import shapefile 
import pandas as pd
import numpy as np
import collections

def getPrecinctData(filename):
    dataframe = pd.read_csv(filename)
    precincts = np.array(dataframe["Precinct"].tolist())
    precinctCounts = np.array(dataframe["Num Crimes"].tolist())
    
    # Dictionary that maps precinct number -> number of crimes
    precinctCrimeDict = dict(zip(dataframe["Precinct"], dataframe["Num Crimes"]))
    indexToPrecinctDict = dict(zip(dataframe["Index"], dataframe["Precinct"]))
    return precinctCrimeDict, indexToPrecinctDict


def checkPrecinct(graph):
	path = 'precincts.shp'
	polygon = shapefile.Reader(path) 
	polygon = polygon.shapes() 

	precinctCrimeDict, indexToPrecinctDict = getPrecinctData('historic_crime.csv')
	polygons = [ shape.points for shape in polygon ]

	edgePrecinctCrimes = collections.defaultdict(int)

	for node in graph.nodes(data=True):
		for i,polygon in enumerate(polygons):
			    poly = Polygon(polygon)
			    latLonPoint = (Point(node[1]['x'], node[1]['y']))
			    if poly.contains(latLonPoint):
			    	precinct = indexToPrecinctDict.get(i)
			    	edgePrecinctCrimes[node[0]] = precinctCrimeDict.get(precinct)
			    	break
	#print "done"

	return edgePrecinctCrimes

def main():

	path = 'precincts.shp'
	polygon = shapefile.Reader(path) 
	polygon = polygon.shapes() 

	precincts, precinctCounts, precinctCrimeDict = getPrecinctData('historic_crime.csv')
	shpfilePoints = [ shape.points for shape in polygon ]
	p_indices = range(34)

	#Dictionary that maps the index of the polygon to the corresponding precinct number
	indexToPrecinct = {}
	for i in range(len(precincts)):
		indexToPrecinct[i] = precincts[i]

	polygons = shpfilePoints
	points = []
	backwards = [(40.7638434, -73.9798564), (40.763845, -73.9798564),
(40.797613299999995, -73.9142585), (40.7976144, -73.9142585),
(40.7451151, -73.97615649999999), 
(40.7121447, -73.9445683), (40.7372527, -73.9398978), (40.737253499999994, -73.9398978)]
	for pt in backwards:
		x = pt[1]
		y = pt[0]
		points.append(Point(x,y))


	#Check if point is in the precinct
	#If it is, print out the precinct number 
	for point in points: 
		for i,polygon in enumerate(polygons):
		    poly = Polygon(polygon)
		    if poly.contains(point):
		    	print 'inside'
		    	precinct = indexToPrecinct.get(i)
		    	print "precinct number is ", precinct
		    	print "num crimes in precinct is ", precinctCrimeDict.get(precinct)


if __name__ == '__main__':
    main()