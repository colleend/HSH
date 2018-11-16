import csv
import random
import collections
import math
import copy 
import sys
import pandas as pd
import numpy as np
import geopy.distance 
SAMPLE_SIZE = 20000

# Loads felony data
# Gets lists of latitudes and longitudes
# For every felony:
# Gets nearest four points 
# Finds closest edge
# Adds closest edge to crimeCount dict 

startingPoint = (40.66245, -73.9494)
nodeList = [(40.7685244,-73.8938515), (40.7685244, -74.0789962), (40.8830659, -73.8938515), (40.883659, -74.0789962)]

def getEdges(nodes):
    edgeSet = []
    copyNodes = copy.copy(nodes)
    for node in nodes: 
        for findNode in copyNodes:
            if node != findNode:
                if node[0] == findNode[0] or node[1] == findNode[1]:
                    edge = (node, findNode)
                    dupEdge = (findNode, node)
                    if edge not in edgeSet and dupEdge not in edgeSet: 
                        edgeSet.append(edge)
    return edgeSet


edgeList = getEdges(nodeList)
def getDistanceDict(startingPoint, edgeList):
	distanceDict = collections.defaultdict(float)
	for edge in edgeList:
		lastNode = edge[1]
		kmDistance = geopy.distance.distance(startingPoint, lastNode).km
		milesDistance = kmDistance*0.621371
		distanceDict[edge] = milesDistance
	return distanceDict

distanceDict = getDistanceDict(startingPoint, edgeList)
print distanceDict