from .conf import DATA_PATH
import os

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
