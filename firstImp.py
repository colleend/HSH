import xml.etree.ElementTree

pathToXML = "/Users/colleendai/Desktop/School/Computer Science/CS221/project/map.xml"

treeRoot = xml.etree.ElementTree.parse(pathToXML).getroot()

nodes = {}
for anode in treeRoot.findall("node"):
	#print (anode.tag, anode.attrib)
	nodeNum = anode.get('id')
	lat = anode.get('lat')
	lon = anode.get('lon')
	if (not nodeNum in nodes):
		nodes[nodeNum] = [1, lat, lon]
	else:
		print ("in els")
		nodes[nodeNum][0] += 1
		break

intersections = []
for nodeNum, info in nodes.iteritems():
	#print (info)
	count, lat, lon = info
	if (count > 1):
		intersections.append((lat, lon))
		print ("intersect found! " + str(info))

print (intersections)


