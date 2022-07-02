import pandas as pd
import numpy as np
import osmnx as ox
import matplotlib.pyplot as plt
import folium
import networkx as nx
from src.osm import OSM

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from src.strava import Strava
# print(ox.__version__)
# print(nx.__version__)

stravaData = Strava.get_shp_data()
stravaData.to_csv('strava.csv')
# Se descarga el mapa de Valparaíso
osmGraph = OSM.get_graph('Valparaíso, Valparaíso, Chile')
osmNodes, osmStreets = ox.graph_to_gdfs(osmGraph, edges = True,fill_edge_geometry=True)

# osmStreets = ox.utils_graph.graph_to_gdfs(osmGraph,nodes = False)
# osmStreets = osmStreets.reset_index()
osmStreetsList = osmStreets[osmStreets["osmid"].apply(lambda reg: isinstance(reg,list))]
osmStreets = osmStreets[~osmStreets["osmid"].apply(lambda reg: isinstance(reg,list))]
osmStreets.to_csv('streets.csv')

stravaStreets = pd.merge(stravaData,osmStreets,left_on = 'osmId',right_on = 'osmid', how = 'inner')
stravaStreets.to_csv("strava_edges.csv",index=False)

# fig,ax = plt.subplots()
# stravaG = stravaStreets['geometry_x'].plot(ax = ax, label = 'VALPARAISO', color = 'grey')
# osmG = osmStreets['geometry'].plot(ax = ax, label = 'PEDALEABLE', color = 'blue')
# plt.show()

#stravaStreets = stravaStreets.set_geometry("geometry_y")
myMap = stravaData.explore()
outfp = r"testStravaMap.html"
myMap.save(outfp)
#edges = nx.Graph.add_edge(stravaStreets['u'], stravaStreets['v'])
# toGraf = ox.graph_from_gdfs(osmNodes,stravaStreets)

# fig,ax = ox.plot.plot_graph(osmGraph)
# fig.savefig('my_figure.svg')
# fig.show()
# ox.folium.plot_graph_folium(toGraf).save('bike_streets.html')
