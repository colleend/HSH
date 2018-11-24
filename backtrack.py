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
        #if (leftIndex != len(absData)-1):
        indices.append(leftIndex)
        #else:
        #    indices.append(leftIndex)
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
        if (pt == (40.766937799999994, -73.9165022)):
            print (closestPoints)
            print (edges)
        for edge in edges:
            if (pt == (40.766937799999994, -73.9165022)):
                print (edge)
            edgesList.append(edge)

    return lats, lons, edgesList

def getAllWeights(edgesList, startingPoint, crimeCounts):
    #df = pd.read_csv(distanceFile, names = ["Edge", "Distance"])
    #distanceDict = df.set_index('Edge')['Distance'].to_dict()
    distanceDict = getDistanceDict(startingPoint, edgesList)
    weights = getWeights(distanceDict, crimeCounts)
    #writeDict(weights, weightsFile)
    return weights

def backtrackingSearch(lats, lons, weights, start, stop):
    # (technicality: using array because of Python scoping)
    bestTotalCost = [float('+inf')]
    bestEdges = [None]
    # CurrentPoint and endPoint are tuples of (lat, lon).
    def recurse(currentPoint, endPoint, weights, edges, totalCost):
        print ("current point" + str(currentPoint))
        # At node having undergone |edges|, accumulated |totalCost|.
        #if ((abs(currentPoint[0]-endPoint[0]) <= 0.01 and abs(currentPoint[1]-endPoint[1]) <= 0.01)):
        if (currentPoint == endPoint):
            # Update the best solution so far
            if totalCost < bestTotalCost[0]:
                print ("in if, totalcost = " + str(totalCost) + " edges = " + str(edges)) 
                bestTotalCost[0] = totalCost
                bestEdges[0] = edges
            return

        # Recurse on neighbor nodes
        for neighbor in getNearestFourPts(currentPoint, lats, lons):
            takenEdge = (currentPoint, neighbor)
            print (takenEdge)
            if (not takenEdge in weights):
                print ("taken Edge not in weights " + str(takenEdge))
                takenEdge = (neighbor, currentPoint)
                if (not takenEdge in weights):
                    print ("taken Edge REALLY not in weights " + str(takenEdge))
                    continue
            cost = weights[takenEdge]
            recurse(neighbor, endPoint, weights, edges + [takenEdge], totalCost + cost)

    recurse(start, stop, weights, edges=[], totalCost=0)
    return (bestTotalCost[0], bestEdges[0])

def main():
    crimeCounts = load_crime_counts(crimeFile)
    lats, lons, edges = getAllEdges(crimeCounts)
    print (len(edges))
    #print (edges[1])
    startingPoint = (40.766937799999994, -73.9165022)
    stoppingPoint = (40.766938200000006, -73.9165022)
    weights = getAllWeights(edges, startingPoint, crimeCounts)
    print (weights[((40.766937799999994, -73.9165022), (40.766938200000006, -73.9165022))])
    print (len(weights))
    print (backtrackingSearch(lats, lons, weights, startingPoint, stoppingPoint))
    
if __name__ == '__main__':
    main()