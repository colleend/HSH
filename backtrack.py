from crime_data import getNearestFourPts
from crime_data import load_crime_data, getIntersections, getEdges, writeDict
from getWeights import getWeights
from edited_manhattan_distance import getDistanceDict
import pandas as pd
import numpy as np

crimeFile = "crimeCounts.csv"
distanceFile = "distance.csv"
weightsFile = "weights.csv"

def getIndices(data, pt, neg):
# Returns index or index range of indices
    absData = data
    indices = []
    if (neg):
        leftIndex = np.searchsorted(absData, pt, side = "right")
    else:
        leftIndex = np.searchsorted(absData, pt, side = "left")

    # Nothing found by searchsorted
    if (leftIndex == len(absData)):
        return indices
    elif (absData[leftIndex] == pt):
        indices.append(leftIndex)
    elif (absData[leftIndex] > pt): 
        indices.append(leftIndex-1)
        if (leftIndex != len(absData)-1):
            indices.append(leftIndex+1)
        else:
            indices.append(leftIndex)
    else:
        raise Exception("FUCK ME UP")

    return indices

def getNearestFourPts(pt, lats, lons):
    attempts = {}
    output = []
    x = float(pt[0])
    y = float(pt[1])

    X_results = getIndices(lats, x, True)
    Y_results = getIndices(lons, y, False)

    if(len(X_results) != 0 and len(Y_results) != 0):
        for i in X_results:
            for j in Y_results:
                output.append((lats[i],lons[j]))
    return output

def load_crime_counts(filename):
    names = ["Edges", "CrimeCounts"]
    df = pd.read_csv(filename, names = names)
    crimeCounts = df.set_index('Edges')["CrimeCounts"].to_dict()
    return crimeCounts

def load_node_locs(filename):
    dataframe = pd.read_csv(filename)
    coordinates = list(zip(dataframe["Latitude"], dataframe["Longitude"]))
    return coordinates

def getAllEdges(crimeCounts):
    data = load_node_locs('nodeLocs.csv')
    lats, lons, intersectionsDict = getIntersections('nodeLocsWithTitles.csv')  
    edgesList = []

    for pt in data:
        closestPoints = getNearestFourPts(pt, lats, lons)
        edges = getEdges(closestPoints)
        for edge in edges:
            edgesList.append(edge)

    return lats, lons, edgesList

def getAllWeights(edgesList, startingPoint, crimeCounts):
    df = pd.read_csv(distanceFile, names = ["Edge", "Distance"])
    distanceDict = df.set_index('Edge')['Distance'].to_dict()
    weights = getWeights(distanceDict, crimeCounts)
    writeDict(weights, weightsFile)
    return weights

def backtrackingSearch(lats, lons, weights, start, stop):
    # (technicality: using array because of Python scoping)
    bestTotalCost = [float('+inf')]
    bestEdges = [None]
    # CurrentPoint and endPoint are tuples of (lat, lon).
    def recurse(currentPoint, endPoint, edges, totalCost):
        # At node having undergone |edges|, accumulated |totalCost|.
        # Explore the neighbors of currentPoint.
        if (abs(currentPoint[0]-endPoint[0]) <= 0.01 and abs(currentPoint[1]-endPoint[1]) <= 0.01):
            # Update the best solution so far
            print ("in if")
            if totalCost < bestTotalCost[0]:
                bestTotalCost[0] = totalCost
                bestEdges[0] = edges
            return

        # Recurse on neighbor nodes
        for neighbor in getNearestFourPts(currentPoint, lats, lons):
            takenEdge = (currentPoint, neighbor)
            if (not str(takenEdge) in weights):
                continue   
            cost = weights[str(takenEdge)]
            print (neighbor)
            recurse(neighbor, endPoint, edges + [takenEdge], totalCost + cost)

    recurse(start, stop, edges=[], totalCost=0)
    return (bestTotalCost[0], bestEdges[0])

def main():
    crimeCounts = load_crime_counts(crimeFile)
    lats, lons, edges = getAllEdges(crimeCounts)
    print (len(edges))
    #print (edges[1])
    startingPoint = (40.766937799999994, -73.9165022)
    stoppingPoint = (40.46245, -73.8400)
    weights = getAllWeights(edges, startingPoint, crimeCounts)
    print (len(weights))
    print (weights.keys()[1])
    print (backtrackingSearch(lats, lons, weights, startingPoint, stoppingPoint))
    
if __name__ == '__main__':
    main()