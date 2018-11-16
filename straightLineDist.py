import sys
import random
import collections
import copy
import math


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

x1 = 1
x2 = 3 
y2 = 5
y3 = 7
p1 = 2
p2 = 5.5
currPoint = (p1, p2)
nodes = [(x1,y2), (x1,y3), (x2,y2), (x2,y3)]
closestEdgeSet = getEdges(nodes)
#[((x1,y2), (x1,y3)), ((x1,y2),(x2,y2)), ((x1,y3),(x2,y3)), ((x2,y2),(x2,y3))]
distances = getStraightLineDist(currPoint, closestEdgeSet)
print distances
shortestEdge = min(distances, key=distances.get)
print shortestEdge