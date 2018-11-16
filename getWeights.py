import sys
import random
import collections
import copy
import math

def getWeights(manhattanDistances, crimeCounts):
	#given dictionary of edge -->manhattandistance and dict of edge --> crimeCounts
	allWeights = {}
	for edge, distance in manhattanDistances.iteritems():
		md = float(1)/float(distance)
		if edge in crimeCounts:
			numCrimes = crimeCounts[edge]
		else:
			numCrimes = 2 
		inverse = float(1)/float(numCrimes)
		weight = md +inverse
		allWeights[edge] = weight
	print allWeights

# manhattanDistances = {
# 	((1,5),(3,5)): 2,
# 	((1,8),(3,8)): 2,
# 	((1,5),(1,8)): 3,
# 	((3,5),(3,8)): 3
# }

# crimeCounts ={
# 	((1,8),(3,8)): 1,
# 	((1,5),(1,8)): 4,
# 	((3,5),(3,8)): 2
# }

getWeights(manhattanDistances,crimeCounts)

