import lxml.etree
import csv
import collections

pathToXML = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/map.xml"
newFileName = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/nodeLocs.csv"
newNodeFileName = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/nodes.csv"

doc = lxml.etree.parse(pathToXML)
treeRoot = doc.getroot()

# Go through all the nodes, make a dictionary of nodeNum -> #occurences
nodes = collections.defaultdict(int)
for anode in treeRoot.findall(".//way//nd"):
	nodeNum = anode.get('ref')
	nodes[nodeNum] += 1

# Get all the intersections (count > 1)
intersections = []
for nodeNum, count in nodes.iteritems():
	if (count > 1):
		intersections.append(nodeNum)

# Write to csv file
with open(newNodeFileName, 'wb') as f:
	nodeWriter = csv.writer(f, delimiter=' ')
	for node in intersections:
		nodeWriter.writerow([node])

# Get a dict of nodeNum : lat, lon
nodeInfo = collections.defaultdict(int)
for anode in treeRoot.findall("node"):	
	nodeNum = anode.get('id')
	lat = anode.get('lat')
	lon = anode.get('lon')
	nodeInfo[nodeNum] = (lon, lat) #Lon x, Lat y

# Write to csv file of intersection node num, lat, lon
with open(newFileName, 'wb') as csvfile:
	locWriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	locWriter.writerow(["NodeNumber", "Latitude", "Longitude"])
	for nodeNum in intersections:
		lon, lat = nodeInfo[nodeNum]
		locWriter.writerow([nodeNum, lat, lon])



