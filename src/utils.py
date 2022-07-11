from .conf import DATA_PATH,URGENCY
import os
import numpy as np
import geopandas as geopd

class Utils: 
    def is_list(element) -> bool:
        if(isinstance(element,list)):
            return True
        return False

    def sum_in_list(element):
        if(isinstance(element,list)):
            sum = 0
            for num in element:
                sum += int(num)
            return sum
        else:
            return element

    def get_file_by_extension(ext:str):
        for obj in os.scandir(DATA_PATH):
            if obj.is_file() and ext in obj.name:
                return os.path.dirname(os.path.realpath(obj.path + os.sep + obj.name))

    def percentage(x,xmax):
        return round((x/xmax * 100),2)

    def classify(x,min,max):
        minUrgency = min * 100
        consider = max - minUrgency
        mediumUrgency = consider * 0.5 + minUrgency
        highUrgency = consider * 0.9 + minUrgency
        
        if(x < minUrgency):
            return URGENCY['minUrgency']
        elif(minUrgency <= x < mediumUrgency):
            return URGENCY['mediumUrgency']
        elif(mediumUrgency <= x < highUrgency):
            return URGENCY['highUrgency']
        else:
            return URGENCY['maxUrgency']

class Shapes:
    def city_polygon(gdf):
        geometries = [i for i in gdf.geometry]

        all_coords = []
        for b in geometries.boundary: # for first feature/row
            coords = np.dstack(b.coords.xy).tolist()
            all_coords.append(*coords)       

        return coords