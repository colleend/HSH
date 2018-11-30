import osmnx as ox
import networkx as nx
from shapely.geometry import box
import pandas as pd
import numpy as np
import collections

crimeCountsFile = "correctCrimeCounts.csv"

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
	writeDict(nearestNodes, crimeCountsFile)
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
	weights = {}
	for edge in edges:
		firstNode = edge["u"]
		secondNode = edge["v"]
		crimeCount = crimeCountsDict[firstNode] + crimeCountsDict[secondNode]
		weights[edge] = crimeCount + graph[firstNode][secondNode]["length"]

	nx.set_edge_attributes(graph, 'weights', weights)

def writeDict (dic, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for key2, value in dic.iteritems():
            writer.writerow([key2, value])


def getShortestPath(start, destination, graph):
	start_node = ox.get_nearest_node(graph, start, method="euclidean")
	end_node = ox.get_nearest_node(graph, destination, method="euclidean") 
	route = nx.shortest_path(G=graph, source=start_node, target=end_node, weight = "weights")
	fig, ax = ox.plot_graph_route(graph, route, origin_point = start, destination_point = destination)

if __name__ == '__main__':
    main()