import osmnx as ox
import networkx as nx
from shapely.geometry import box
import pandas as pd
import numpy as np
import collections
import csv
from check_precinct import checkPrecinct
import math
from backtrackingCSP import create_csp, run_csp

crimeCountsFile = "correctCrimeCounts.csv"
source = (40.773006, -73.981857) #(40.792820, -73.943835) #(40.744750, -73.995148) #(40.775150, -73.981921)
dest = (40.774143, -73.984840) #(40.831564, -73.946945) #(40.733044, -73.984506) #(40.769057, -73.982266)
#source = (40.744750, -73.995148)
#dest = (40.733044, -73.984506)
FairfaxHotel = (40.756757, -73.992702)
LadureeRes = (40.724689, -74.002391)

def main():
	# Get city graph
	cityStreets = ox.graph_from_place('Manhattan, New York City, New York, USA')
	crimeWeightsDict = readCrimeWeights()
	edges = ox.graph_to_gdfs(cityStreets, nodes=False, edges=True)
	nodes = ox.graph_to_gdfs(cityStreets, nodes=True, edges=False)

	precinctDict = getPrecinctWeights(cityStreets,nodes)
	addWeightsToGraph(cityStreets, crimeWeightsDict, precinctDict, edges)

	#create_csp(cityStreets, source, dest, crimeWeightsDict)
	#run_csp(crimeWeightsDict, cityStreets)

	getShortestPath(FairfaxHotel, LadureeRes, cityStreets, False)

def readCrimeWeights ():
	names = ["NodeNum", "CrimeCount"]
	crimeWeightsData = pd.read_csv(crimeCountsFile, names = names)
	crimeCountsDict = collections.defaultdict(int)
	for index, row in crimeWeightsData.iterrows():
		crimeCountsDict[row['NodeNum']] = row["CrimeCount"]

	return crimeCountsDict

def getCrimeWeights (cityStreets):
	# Get crime data points
	data = load_crime_data('felonies3.csv')
	nearestNodes = collections.defaultdict(int)
	for index, pt in enumerate(data):
		# Get nearest node to data
		nearest = ox.get_nearest_node(cityStreets, pt, method="euclidean")
		nearestNodes[nearest] += 1

	print(nearestNodes)
	writeDict(nearestNodes, crimeCountsFile)

def load_crime_data(filename):
    coordinates = []
    names = ["Latitude", "Longitude", "Points"]
    dataframe = pd.read_csv(filename, names = names)
    lats = np.array(dataframe["Latitude"].tolist())
    lons = np.array(dataframe["Longitude"].tolist())

    coordinates = list(zip(dataframe["Latitude"], dataframe["Longitude"]))
    return coordinates

def getPrecinctWeights (graph, nodes):
	return checkPrecinct(graph)

def addWeightsToGraph (graph, crimeCountsDict, precinctDict, edges):
	# for every edge in the graph, change the weight to be crimecounts of the two nodes in the edge
	weights = {}
	print(edges)
	for edge in graph.edges.data(keys=True):
		firstNode = edge[0]
		secondNode = edge[1]
		crimeCount = crimeCountsDict[firstNode] + crimeCountsDict[secondNode]
		precinctCount = precinctDict[firstNode] + precinctDict[secondNode]
		#print (edge[3]['length'])
		#print (crimeCount)

		edge[3]['weights'] = 3*crimeCount + edge[3]['length'] +  3*math.log1p(precinctCount)
		#edge[3]['weights'] = crimeCount + edge[3]['length'] +  math.log1p(precinctCount)

def writeDict (dic, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for key2, value in dic.iteritems():
            writer.writerow([key2, value])

def getShortestPath(start, destination, graph, straight):
	start_node = ox.get_nearest_node(graph, start, method="euclidean")
	end_node = ox.get_nearest_node(graph, destination, method="euclidean") 
	if (straight):
		route = nx.shortest_path(G=graph, source=start_node, target=end_node, weight = "length")
	else:
		route = nx.shortest_path(G=graph, source=start_node, target=end_node, weight = "weights")
		print (route)
	fig, ax = ox.plot_graph_route(graph, route, origin_point = start, destination_point = destination)

if __name__ == '__main__':
    main()