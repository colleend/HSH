import xml.etree.ElementTree

pathToXML = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/map.xml"

treeRoot = xml.etree.ElementTree.parse(pathToXML).getroot()

nodes = {}
for anode in treeRoot.findall("node"):
	#print (anode.tag, anode.attrib)
	nodeNum = anode.get('id')
	if (not nodeNum in nodes):
		nodes[nodeNum] = 1
	else:
		nodes[nodeNum] += 1

intersections = []
for nodeNum, count in nodes:
	if (count > 1):
		intersections.append(nodeNum)
		print ("intersect found! " + str(nodeNum))

print (intersections)


