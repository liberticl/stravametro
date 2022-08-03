from .classes.strava import Strava
from .classes.utils import Shapes,Utils
from .classes.osm import Maps, Convert
from .classes.conf import COLNAME, DATA_PATH
from .classes.draw import Export
import geopandas as geopd
import pandas as pd
import numpy as np
import os

import matplotlib
import mapclassify
import folium
import matplotlib.pyplot as plt

# Get GeoData
cityPolygon = Maps.get_place_polygon('Viña del Mar, Valparaíso, Chile')
polygon = cityPolygon['geometry'][0]

def flow(all:bool,year = None):
    # Get by year
    if(all):
        dirs = [dir[0] for dir in os.walk(DATA_PATH)]
        dirs.remove(DATA_PATH)
    else:
        dirs = [DATA_PATH + os.sep + str(year)]
    
    stravaEdges = geopd.GeoDataFrame()
    for dir in dirs:
        if(len(os.listdir(dir)) > 0):
            stravaEdges = geopd.GeoDataFrame(pd.concat([Strava.get_shp_data(dir),stravaEdges]))

    ############################# MAPA CON RUTAS MÁS TRANSITADAS ########################################
    # Get trip data
    tripsData = pd.DataFrame()
    for dir in dirs:
        if(len(os.listdir(dir)) > 0):
            tripsData = pd.concat([Strava.get_csv_data(dir),tripsData])
    tripsData = tripsData[['edge_uid','forward_trip_count','reverse_trip_count']]

    # Calculate totals
    tripsData['total_trip_count'] = tripsData['forward_trip_count'] + tripsData['reverse_trip_count']
    sumByEdges = tripsData.groupby('edge_uid',sort = False).sum()
    sumByEdges = sumByEdges[['total_trip_count']].sort_values('total_trip_count').reset_index()

    # Intersect Data
    cityTrips = pd.merge(stravaEdges,sumByEdges,how = 'inner', left_on = 'edgeUID', right_on = 'edge_uid')
    cityTrips = cityTrips[['osmId','edgeUID','total_trip_count','geometry']]
    cityTrips = cityTrips[~cityTrips.isnull()].reset_index(drop = True)
    cityTrips = geopd.GeoDataFrame(cityTrips)

    # Intersect GeoData
    stravaCity = cityTrips.intersection(polygon) 

    # Union data + geodata
    stravaCity = cityTrips.join(stravaCity.to_frame())
    del stravaCity['geometry']
    stravaCity = stravaCity.rename(columns = {0:'geometry'})
    stravaCity = stravaCity[~stravaCity['geometry'].is_empty].sort_values('total_trip_count').reset_index(drop = True)

    # Getting streets most used
    minTrips = stravaCity['total_trip_count'].min()
    maxTrips = stravaCity['total_trip_count'].max()
    stravaCity[COLNAME['urgency']] = stravaCity['total_trip_count'].apply(lambda x: Utils.classify(x,minTrips,maxTrips))
    stravaCity = stravaCity[['osmId','edgeUID','total_trip_count',COLNAME['urgency'],'geometry']]
    stravaCity.to_csv('Result.csv')

    Export.to_html(stravaCity,cityPolygon,str(year))


def cuantitative():
    dirs = [dir[0] for dir in os.walk(DATA_PATH)]
    dirs.remove(DATA_PATH)

    # Get trip data
    tripsData = pd.DataFrame()
    for dir in dirs:
        if(len(os.listdir(dir)) > 0):
            tripsData = pd.concat([Strava.get_csv_data(dir),tripsData])
    edges = tripsData[['edge_uid']].count().values[0]
    tripsData = tripsData[['year','forward_trip_count','reverse_trip_count']]

    # Calculate totals
    tripsData['total_trip_count'] = tripsData['forward_trip_count'] + tripsData['reverse_trip_count']
    tripsData['media'] = tripsData['total_trip_count']/edges
    sumByYear = tripsData.groupby('year',sort = True).sum()
    
    # Plot travels
    plt.grid()
    plt.plot(sumByYear.index, sumByYear["media"])
    plt.xticks(sumByYear.index,list(sumByYear.index))
    plt.title('Promedio de viajes por calle en Viña del Mar')
    plt.show()

    # Plot travels
    plt.grid()
    plt.plot(sumByYear.index, sumByYear["total_trip_count"])
    plt.xticks(sumByYear.index,list(sumByYear.index))
    plt.title('Total de viajes contabilizados en todas las calles de Viña del Mar')
    plt.show()
