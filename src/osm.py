from audioop import mul
from . import utils
from .conf import ERR_MSG
import pandas as pd
import geopandas as geopd
import osmnx as ox
import pandas as pd
from shapely.geometry import shape
import requests



class Maps:

    def get_graph(place,mode = 'all', only_edges = True):
        graph = ox.graph_from_place(place, network_type = mode)
        if(only_edges):
            _,edges = ox.graph_to_gdfs(graph, edges = True,fill_edge_geometry=True, clean_periphery = True)
            return edges
        return graph

    def get_osm_relation(place:str):
        url = f'https://nominatim.openstreetmap.org/search?q={place}&format=json'
        ans = requests.get(url)
        data = ans.json()
        
        for element in data:
            if(element['type'] == 'administrative'):
                return element['osm_id']
        
        raise Exception(ERR_MSG['non-existent place'])

    def get_place_polygon(place):
        relation = Maps.get_osm_relation(place)
        url = f'http://polygons.openstreetmap.fr/get_geojson.py?id={relation}&params=0'
        ans = requests.get(url)  
        gdf = geopd.read_file(ans.text)
        gdf = gdf.explode(index_parts = False)
        return gdf

    def list_to_single_id(streets):
        streets["id_in_list"] = streets["osmid"].apply(lambda osmid: utils.is_list(osmid))
        toExport = streets[streets["id_in_list"] == False]

        toModify = streets[streets["id_in_list"] == True]
        toModify = toModify.explode("osmid")
        # Corregir esta línea!!
        toModify["oneway"] = toModify[["oneway","lanes"]].apply(lambda row: False if utils.is_list(row["lanes"]) else row["oneway"])
        toModify["lanes"] = toModify["lanes"].apply(lambda lanes: utils.sum_in_list(lanes))
        toModify.to_csv('test.csv')
        return toModify


class Convert:

    def place_to_df(place: str, mode = 'bike', save = False, save_as = 'csv'):
        #place = 'Valparaíso, Valparaíso, Chile'
        osmGraph = OSM.get_graph(place,network_type = mode)
        osmStreets = ox.utils_graph.graph_to_gdfs(osmGraph,nodes = False)
        if(save):
            if(save_as.split('.')[-1] == 'csv'):
                osmStreets.to_csv(save_as)
            elif(save_as.split('.')[-1] == 'xlsx'):
                osmStreets.to_excel(save_as)
            else:
                raise Exception(ERR_MSG['not_supported'])
        return osmStreets

    def to_polygon(gdf):
        if 'geometry' not in gdf.columns:
            raise Exception(ERR_MSG['missing_column'] + ' geometry')
        else:
            #gdf['points'] = gdf['geometry'].boundary
            multiLine = gdf['geometry'].unary_union
            polygon = multiLine.convex_hull
            new_gdf = geopd.GeoSeries(polygon)
            return new_gdf
