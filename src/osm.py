from . import utils
from .conf import ERR_MSG
import pandas as pd
import osmnx as ox



class OSM:

    def get_graph(place,mode = 'bike'):
        return ox.graph_from_place(place, network_type = mode)

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

