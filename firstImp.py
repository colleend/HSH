import lxml.etree
import collections

pathToXML = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/map.xml"

treeRoot = lxml.etree.parse(pathToXML).getroot()

nodes = collections.defaultdict(int)
for anode in treeRoot.findall("./way/nd"):
	nodeNum = anode.get('ref')
	nodes[nodeNum] += 1

intersections = []
for nodeNum, count in nodes.iteritems():
	if (count > 1):
		intersections.append((nodeNum))

print (intersections)


