from .utils import Utils
import geopandas as geopd
import pandas as pd


class Strava:
    def get_shp_data():
        shpFile = Utils.get_file_by_extension('shp')
        return geopd.read_file(shpFile)

    def get_csv_data():
        csvFile = Utils.get_file_by_extension('csv')
        return pd.read_csv(csvFile,low_memory = False)