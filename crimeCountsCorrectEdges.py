import osmnx as ox
import networkx as nx
from shapely.geometry import box
import pandas as pd
import numpy as np
import collections

def main():
	# Get city graph
	cityStreets = ox.graph_from_place('Manhattan, New York City, New York, USA')
	edges = ox.graph_to_gdfs(cityStreets, nodes=False, edges=True)
	nodes = ox.graph_to_gdfs(cityStreets, nodes=True, edges=False)
	print(edges.head())

	# Get crime data points
	data = load_crime_data('felonies3.csv')
	nearestNodes = collections.defaultdict(int)
	for index, pt in enumerate(data):
		# Get nearest node to data
		nearest = ox.get_nearest_node(cityStreets, pt, method="euclidean")
		nearestNodes[nearest] += 1

	print(nearestNodes)
	bbox = box(*edges.unary_union.bounds)
	print (bbox)

	addWeightsToGraph(cityStreets, nearestNodes)


def load_crime_data(filename):
    coordinates = []
    names = ["Latitude", "Longitude", "Points"]
    dataframe = pd.read_csv(filename, names = names)
    lats = np.array(dataframe["Latitude"].tolist())
    lons = np.array(dataframe["Longitude"].tolist())

    coordinates = list(zip(dataframe["Latitude"], dataframe["Longitude"]))
    return coordinates

def addWeightsToGraph (graph, crimeCountsDict):
	# for every edge in the graph, change the weight to be crimecounts of the two nodes in the edge
	for edge in edges:
		firstNode = edge["u"]
		secondNode = edge["v"]
		crimeCount = crimeCountsDict[firstNode] + crimeCountsDict[secondNode]
		graph[firstNode][secondNode]["weight"] = crimeCount

def getShortestPath ()


if __name__ == '__main__':
    main()