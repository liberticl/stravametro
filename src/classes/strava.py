from .utils import Utils
from .filter import byTime
import geopandas as geopd
import pandas as pd
import os

class Strava:
    def get_shp_data(pathName:str):
        shpFile = Utils.get_file_by_extension('shp',pathName)
        return geopd.read_file(shpFile)

    def get_csv_data(pathName:str, day = None, hourRange = None):
        csvFile = Utils.get_file_by_extension('csv',pathName)
        data = pd.read_csv(csvFile,low_memory = False)
        if(day or hourRange):
            data = byTime.hour_range(data, hourRange, day)
        return data
