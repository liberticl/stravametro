from .utils import Utils
import geopandas as geopd
import pandas as pd
import os


class Strava:
    def get_shp_data(pathName:str):
        shpFile = Utils.get_file_by_extension('shp',pathName)
        return geopd.read_file(shpFile)

    def get_csv_data(pathName:str):
        csvFile = Utils.get_file_by_extension('csv',pathName)
        return pd.read_csv(csvFile,low_memory = False)
