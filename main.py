import pandas as pd
import numpy as np
import geopandas as geopd
import osmnx as ox
import matplotlib.pyplot as plt
import folium


stravaData = geopd.read_file('a194d8ef5e9c573f43e8b74b21aea76dff15c3409636491028c2f4099e62fb79-1629079624795.shp')

place = 'Valparaíso, Valparaíso, Chile'
osmGraph = ox.graph_from_place(place, network_type='bike')
osmNodes, osmStreets = ox.graph_to_gdfs(osmGraph)

count = pd.DataFrame()
count["osmid"] = osmStreets["osmid"].apply(lambda l: len(l) if type(l) == list else 0)
count["name"] = osmStreets["name"].apply(lambda l: len(l) if type(l) == list else 0)
count["highway"] = osmStreets["highway"].apply(lambda l: len(l) if type(l) == list else 0)
count = count[(count > 0).any(axis=1)]
count["id-name"] = np.where(count["osmid"] == count["name"],True,False)
count["id-highway"] = np.where(count["osmid"] == count["highway"],True,False)
print(len(stravaData))
print(len(osmStreets))
print(len(count[count["osmid"] > 0]))
print(str(len(count[count["osmid"] > 0])/len(stravaData)*100)+'%')
print(str(len(count[count["osmid"] > 0])/len(osmStreets)*100)+'%')
print(len(count[count["id-name"] == True]))
print(len(count[count["id-highway"] == True]))
# osmStreets.to_csv('streets.csv')
# osmNodes.to_csv('nodes.csv')

# stravaStreets = pd.merge(stravaData,osmStreets,left_on = 'osmId',right_on = 'osmid', how = 'inner')
# print(stravaStreets)#.to_csv("test.csv",index=False)



#mapData = pd.read_csv('a194d8ef5e9c573f43e8b74b21aea76dff15c3409636491028c2f4099e62fb79-1629079624795.csv')

#print(mapData.head())


# shpData.to_csv('strava.csv')

# toGraf = ox.utils_graph.graph_from_gdfs(shpData["osmId"])
# print(type(toGraf))

# print(type(graph))

# streets.to_csv('streets.csv')
# nodes.to_csv('nodes.csv')
# fig,ax = ox.plot.plot_graph(graph)
# fig.savefig('my_figure.svg')
# fig.show()
#ox.folium.plot_graph_folium(graph).save('bike_streets.html')
