from .utils import Utils
import geopandas as geopd


class Strava:
    def get_shp_data():
        shpFile = Utils.get_file_by_extension('shp')
        return geopd.read_file(shpFile)
