import osmnx as ox
import networkx as nx
city = ox.gdf_from_place('Manhattan, New York City, New York, USA')
#ox.plot_shape(ox.project_gdf(city))

cityStreets = ox.graph_from_place('Manhattan, New York City, New York, USA')
ox.plot_graph(cityStreets)
edges = ox.graph_to_gdfs(city, nodes=False, edges=True)
nodes = ox.graph_to_gdfs(city, nodes=True, edge=False)
print(edges.head())

