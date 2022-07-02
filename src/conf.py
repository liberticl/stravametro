import yaml
import os


class Env:
    def get():
        for obj in os.scandir(ROOTDIR):
            if obj.is_file() and 'env' in obj.name:
                return os.path.dirname(os.path.realpath(obj.path + os.sep + obj.name))

    def lang():
        with open(Env.get()) as file:
            env = yaml.load(file,Loader = yaml.FullLoader)
        return env['lang']

class Path:
    def get_names(key:str):
        with open(Env.get()) as file:
            env = yaml.load(file,Loader = yaml.FullLoader)
        return env['path_names'][key]
    
    def get(key:str):
        try: 
            for obj in os.scandir(ROOTDIR):
                if obj.is_dir() and Path.get_names(key) in obj.name:
                    return os.path.dirname(os.path.realpath(obj.path + os.sep + obj.name))
        except:
            raise Exception(f"{key} directory does not exist in {ROOTDIR}!")


class Lang:
    def use():
        lang = Env.lang()
        file = "/" + lang + ".yaml"
        with open(Path.get('lang') + file) as language:
            return yaml.load(language,Loader = yaml.FullLoader)

    def errors():
        messages = Lang.use()
        return messages['errors']

ROOTDIR = 'src'
DATA_PATH = Path.get('data')
ERR_MSG = Lang.errors()
