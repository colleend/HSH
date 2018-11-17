import csv
import random
import collections
import math
import copy 
import sys
import pandas as pd
import numpy as np
SAMPLE_SIZE = 20000

# Loads felony data
# Gets lists of latitudes and longitudes
# For every felony:
# Gets nearest four points 
# Finds closest edge
# Adds closest edge to crimeCount dict 

crimeCountsFile = "crimeCounts.csv"
distanceFile = "distances.csv"
#startingPoint = (40.766937799999994, -73.9165022)

def main():
    data = load_crime_data('felonies2.csv', 'new.csv')
    lats, lons, intersectionsDict = getIntersections('nodeLocsWithTitles.csv')
    data = data[:2000]
    #print (data)

    crimeCounts = {}
    for pt in data:
       float_pt = (float(pt[0]), float(pt[1]))
       results = getNearestFourPts(pt, lats, lons)
       edges = getEdges(results)
       distances = getStraightLineDist(float_pt, edges)

       if distances != {}:
           shortestEdge = min(distances, key=distances.get)
           if shortestEdge in crimeCounts:
                crimeCounts[shortestEdge] += 1
           else: 
                crimeCounts[shortestEdge] = 1

    writeDict(crimeCounts, crimeCountsFile)

    #distanceDict = getDistanceDict(startingPoint, crimeCounts.keys())
    #writeDict(distanceDict, distanceFile)

# Takes data from filename and randomly shuffles it. 
# Writes new data in filename2 with SAMPLE_SIZE rows
def load_crime_data(filename, filename2, write=False):
    coordinates = []
    names = ["Latitude", "Longitude", "Points"]
    dataframe = pd.read_csv(filename, names = names)
    lats = dataframe["Latitude"].tolist()
    lons = dataframe["Longitude"].tolist()
    #print (dataframe)
    #print (lats)
    lats = np.array(lats)
    lons = np.array(lons)
    coordinates = list(zip(dataframe["Latitude"], dataframe["Longitude"]))

    '''with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            lat = row[0]
            lon = row[1]
            if(write): coordinates.append([latlon]) #list format
            else: coordinates.append((lat, lon)) #tuple format'''

    random.shuffle(coordinates) #shuffles all coordinates
    #data = coordinates[:SAMPLE_SIZE] #sample the data 


# Writes new CSV file with sampled crime data
    '''if(write):
        with open(filename2, 'wb') as f2:
            writer = csv.writer(f2)
            count = 0
            for row in coordinates:
                #pick random 20000 crimes
                if count > SAMPLE_SIZE: break
                writer.writerow(float(row))
                count +=1
        f2.close()
    f.close()'''
    return coordinates

# Gets the intersection vectors
def getIntersections(filename):
    dataframe = pd.read_csv(filename, sep = ' ')
    lats = set(dataframe["Latitude"].tolist())
    lons = set(dataframe["Longitude"].tolist())
    lats = np.absolute(np.array(sorted(lats)))
    lons = np.absolute(np.array(sorted(lons)))

    intersectionsDict = list(zip(dataframe["Latitude"], dataframe["Longitude"]))

    return lats, lons, intersectionsDict

def getIndices(data, pt):
# Returns index or index range of 
    absData = np.abs(data)
    indices = []
    leftIndex = np.searchsorted(absData, abs(pt), side = "left")
    if (leftIndex == len(absData)):
        indices.append(len(data)-1)
    elif (absData[leftIndex] == abs(pt)):
        indices.append(leftIndex)

    elif (absData[leftIndex] > abs(pt)): 
        indices.append(leftIndex+1)
        indices.append(leftIndex)
    else:
        throw (Exception("FUCK ME UP"))

    return indices
    #indices = []
   # print ("data point" + str(pt))
    #gprint ("largest " + str(data[-1]))
    '''for i in range(len(data)-1):
        #print i
        if abs(data[i]) == abs(pt): 
            indices.append(i)
            return indices
        elif abs(data[i]) > abs(pt): 
            indices.append(i-1)
            indices.append(i)
            return indices
    return indices'''

def getNearestFourPts(pt, lats, lons):
    attempts = {}
    output = []
    x = float(pt[0])
    y = float(pt[1])

    X_results = getIndices(lats, x)
    Y_results = getIndices(lons, y)

    if(len(X_results) != 0 and len(Y_results) != 0):
        # for i in X_results:
        #     output.append(lats[i])
        # for j in Y_results:
        #     output.append(lons[j])
        for i in X_results:
            for j in Y_results:
                output.append((lats[i],lons[j]))
    return output



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


def getStraightLineDist(currPoint, closestEdgeSet):
    distances = {} #edge -> distance 
    dist = 0
    for edge in closestEdgeSet: 
        point1 = edge[0]
        point2 = edge[1]
        if point2[0] - point1[0] != 0:
            slope = float((point2[1]-point1[1]))/float((point2[0]-point1[0]))
            x = point1[0]
            y = point1[1]
            b = float(y) - float(slope*x)
            #have equation of line 
            m = currPoint[0] 
            n = currPoint[1]
            dist = abs((slope*m) + ((-1)*n) + b)/math.sqrt(slope**2 + (-1)**2)
        else: #vertical line
            dist = abs(currPoint[0] - point1[0])
        # y = mx+b
        #need to solve for b
        distances[edge] = dist
    return distances

def writeDict (dic, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for key2, value in dic.iteritems():
            writer.writerow([key2, value])

def getDistanceDict (startingPoint, edgeList):
    distanceDict = collections.defaultdict(float)
    print (edgeList)
    for edge in edgeList:
        lastNode = edge[1]
        mandistance = (abs(startingPoint[0]) - abs(lastNode[0]))**2 + (abs(startingPoint[1])-abs(lastNode[1]))**2
        distance = math.sqrt(mandistance)
        distanceDict[edge] = distance
    return distanceDict

    
if __name__ == '__main__':
    main()