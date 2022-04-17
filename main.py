import pandas as pd
import osmnx as ox
import folium

#mapData = pd.read_csv('a194d8ef5e9c573f43e8b74b21aea76dff15c3409636491028c2f4099e62fb79-1629079624795.csv')

#print(mapData.head())

place = 'Valparaíso, Valparaíso, Chile'
# tags = {'amenity': 'cafe'}
# cafe = ox.geometries_from_place(place, tags=tags)
# cafe.to_csv('test.csv')

# cafe_points = cafe[cafe.geom_type == 'Point']

# m = folium.Map([-71.6277909,-33.0426659], zoom_start=10)
# locs = zip(cafe_points.geometry.y, cafe_points.geometry.x)

# for location in locs:
#     folium.CircleMarker(location=location).add_to(m)
#     m.save('cafes.html')

graph = ox.graph_from_place(place, network_type='drive')
nodes, streets = ox.graph_to_gdfs(graph)
streets.to_csv('streets.csv')
ox.folium.plot_graph_folium(graph).save('streets.html')