from wsgiref import headers
from .conf import URGENCY
import os
import numpy as np
import geopandas as geopd
import requests

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

    def get_file_by_extension(ext:str,path:str):
        for obj in os.scandir(path):
            if obj.is_file() and ext in obj.name:
                return os.path.dirname(os.path.realpath(obj.path + os.sep + obj.name))

    def classify(x,min,max):
        minUrgency = min * 100
        consider = max - minUrgency
        mediumUrgency = consider * 0.5 + minUrgency
        highUrgency = consider * 0.8 + minUrgency
        
        if(x < minUrgency):
            return URGENCY['minUrgency']
        elif(x < mediumUrgency):
            return URGENCY['mediumUrgency']
        elif(x < highUrgency):
            return URGENCY['highUrgency']
        elif(x >= highUrgency):
            return URGENCY['maxUrgency']
        else:
            return URGENCY['unclassified']

    def get_key_by_value(aDict:dict,value:str):
        for key,val in aDict.items():
            if(val == value):
                return key
        return False

class Shapes:
    def city_polygon(gdf):
        geometries = [i for i in gdf.geometry]

        all_coords = []
        for b in geometries.boundary: # for first feature/row
            coords = np.dstack(b.coords.xy).tolist()
            all_coords.append(*coords)       

        return coords

class StrUtils:
    def replace_accents(string:str):
        toReturn = string.replace('á','a').replace('Á','A')
        toReturn = toReturn.replace('é','e').replace('É','E')
        toReturn = toReturn.replace('í','i').replace('Í','I')
        toReturn = toReturn.replace('ó','o').replace('Ó','O')
        toReturn = toReturn.replace('ú','u').replace('Ú','U')
        return toReturn

class GobApi:
    ## https://apis.digital.gob.cl/dpa/
    headers = dict()
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"

    def get_region_by_name(name):
        url = "https://apis.digital.gob.cl/dpa/regiones"
        ans = requests.get(url,headers = GobApi.headers)
        data = ans.json()

        for region in data:
            thisName = StrUtils.replace_accents(region["nombre"])
            if((thisName.lower() in name) or (name in thisName.lower())):
                return (region["codigo"],region["nombre"])

    def get_commune_by_region(name,region):
        regionCode,regionName = GobApi.get_region_by_name(region)
        url = f"https://apis.digital.gob.cl/dpa/regiones/{regionCode}/comunas"
        ans = requests.get(url,headers = GobApi.headers)
        data = ans.json()

        for commune in data:
            thisName = StrUtils.replace_accents(commune["nombre"])
            if((thisName.lower() in name) or (name in thisName.lower())):
                return commune["nombre"] + ', ' + regionName + ', Chile'

    def get_all_communes_in_region(region):
        regionCode,regionName = GobApi.get_region_by_name(region)
        url = f"https://apis.digital.gob.cl/dpa/regiones/{regionCode}/comunas"
        ans = requests.get(url,headers = GobApi.headers)
        data = ans.json()

        all = []
        for commune in data:
            all.append(commune["nombre"] + ', ' + regionName + ', Chile')
        
        return all