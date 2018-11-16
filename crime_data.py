import csv
import random
import collections
import math
import copy 
import sys
SAMPLE_SIZE = 20000

# Loads felony data
# Gets lists of latitudes and longitudes
# For every felony:
# Gets nearest four points 
# Finds closest edge
# Adds closest edge to crimeCount dict 
def main():
    data = load_crime_data('felonies2.csv', 'new.csv')
    #print data
    lats, lons, all_coords = getIntersections('nodeLocs.csv')
    #data = data[:200]

    crimeCounts = {}
    for pt in data:
       #print pt
       float_pt = (float(pt[0]), float(pt[1]))
       results = getNearestFourPts(pt, lats, lons, all_coords)
       edges = getEdges(results)
       distances = getStraightLineDist(float_pt, edges)

       if distances != {}:
           shortestEdge = min(distances, key=distances.get)
           if shortestEdge in crimeCounts:
                crimeCounts[shortestEdge] += 1
           else: 
                crimeCounts[shortestEdge] = 1

    print crimeCounts


       

# Takes data from filename and randomly shuffles it. 
# Writes new data in filename2 with SAMPLE_SIZE rows
def load_crime_data(filename, filename2, write=False):
    coordinates = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            lat = row[0]
            lon = row[1]
            if(write): coordinates.append([latlon]) #list format
            else: coordinates.append((lat, lon)) #tuple format

    random.shuffle(coordinates) #shuffles all coordinates
    data = coordinates[:SAMPLE_SIZE] #sample the data 


# Writes new CSV file with sampled crime data
    if(write):
        with open(filename2, 'wb') as f2:
            writer = csv.writer(f2)
            count = 0
            for row in coordinates:
                #pick random 20000 crimes
                if count > SAMPLE_SIZE: break
                writer.writerow(float(row))
                count +=1
        f2.close()
    f.close()
    return data

# Colleen has a shorter version of this lmao
def getIntersections(filename):
    lats = []
    lons= []
    all_coords = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            new_row = ''.join(row)
            split = new_row.split()
            node = float(split[0])
            lat_i = float(split[1])
            lon_i = float(split[2])
            lats.append(lat_i)
            lons.append(lon_i)
            all_coords[(lat_i, lon_i)] = node

    lats = sorted(lats)
    lons = sorted(lons)
    return lats, lons, all_coords

def getIndices(data, pt):
# Returns index or index range of 
    indices = []
   # print ("data point" + str(pt))
    #gprint ("largest " + str(data[-1]))
    for i in range(len(data)-1):
        #print i
        if abs(data[i]) == abs(pt): 
            indices.append(i)
            return indices

        elif abs(data[i]) > abs(pt): 
            indices.append(i-1)
            indices.append(i)
            return indices

    return indices

def getNearestFourPts(pt, lats, lons, all_coords):
    attempts = {}
    output = []
    x = float(pt[0])
    y = float(pt[1])

    X_results = getIndices(lats, x)
    Y_results = getIndices(lons, y)

    if(X_results != [] and Y_results != []):
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

    

        
    





if __name__ == '__main__':
    main()