import lxml.etree
import collections

pathToXML = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/map.xml"

treeRoot = lxml.etree.parse(pathToXML).getroot()

nodes = collections.defaultdict(int)
for anode in treeRoot.findall(".//way//nd"):
	nodeNum = anode.get('ref')
	nodes[nodeNum] += 1

intersections = []
for nodeNum, count in nodes.iteritems():
	if (count > 1):
		intersections.append(nodeNum)

locNodes = []
print (intersections)
'''for nodeNum in intersections:
	searchstring = ".//node/..[@id='%s']" %nodeNum
	node = treeRoot.find(searchstring)
	lat = node.get('lat')
	lon = node.get('lon')
	num = node.get('id')
	locNodes.append([num, lat, lon])'''
'''for node in treeRoot.findall(".//node"):
	num = int(node.get('id'))
	if (num in intersections):
		lat = node.get('lat')
		lon = node.get('lon')
		locNodes.append([num, lat, lon])'''


