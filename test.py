from dbm import dumb
from src.strava import Strava
from src.utils import Shapes,Utils
from src.osm import Maps, Convert
from src.conf import COLNAME
import osmnx as ox
import geopandas as geopd
import pandas as pd
import numpy as np
import shapely.speedups

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

import folium

# Get GeoData
cityPolygon = Maps.get_place_polygon('Valparaíso, Valparaíso, Chile')
polygon = cityPolygon['geometry'][0]
stravaEdges = Strava.get_shp_data()

# # Intersect GeoData
# stravaCity = stravaEdges.intersection(polygon)

# # Plot and get HTML
# stravaMap = stravaCity.explore()
# cityPolygon.explore(m = stravaMap, color = 'gray')
# folium.TileLayer('Stamen Toner', control=True).add_to(stravaMap)  # use folium to add alternative tiles
# folium.LayerControl().add_to(stravaMap)  # use folium to add layer control
# outfp = r"testMap.html"
# stravaMap.save(outfp)


############################# MAPA CON RUTAS MÁS TRANSITADAS ########################################
# Get trip data
tripsData = Strava.get_csv_data()
tripsData = tripsData[['edge_uid','forward_trip_count','reverse_trip_count']]

# Calculate totals
tripsData['total_trip_count'] = tripsData['forward_trip_count'] + tripsData['reverse_trip_count']
sumByEdges = tripsData.groupby('edge_uid',sort = False).sum()
sumByEdges = sumByEdges[['total_trip_count']].sort_values('total_trip_count').reset_index()

# Getting streets most used
minTrips = sumByEdges['total_trip_count'].min()
maxTrips = sumByEdges['total_trip_count'].max()
sumByEdges[COLNAME['urgency']] = sumByEdges['total_trip_count'].apply(lambda x: Utils.classify(x,minTrips,maxTrips))

# Intersect Data
cityTrips = pd.merge(stravaEdges,sumByEdges,how = 'inner', left_on = 'edgeUID', right_on = 'edge_uid')
cityTrips = cityTrips[['osmId','edgeUID','total_trip_count',COLNAME['urgency'],'geometry']]
cityTrips = cityTrips[~cityTrips.isnull()].reset_index(drop = True)
cityTrips = geopd.GeoDataFrame(cityTrips)

# Intersect GeoData
stravaCity = cityTrips.intersection(polygon) 

# Union data + geodata
stravaCity = cityTrips.join(stravaCity.to_frame())
del stravaCity['geometry']
stravaCity = stravaCity.rename(columns = {0:'geometry'})
stravaCity = stravaCity[~stravaCity['geometry'].is_empty].sort_values('total_trip_count').reset_index(drop = True)

# Plot travels
# plt.grid()
# plt.plot(stravaCity.index, stravaCity["total_trip_count"])
# plt.show()

# Plot and get HTML
stravaMap = stravaCity.explore(
    column = COLNAME['urgency'],
    tooltip = COLNAME['urgency'],
    popup = True,
    cmap = 'rainbow'
)
# cityPolygon.explore(m = stravaMap, color = 'gray')
outfp = r"tripsMap.html"
stravaMap.save(outfp)