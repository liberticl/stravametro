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

    def mapcolors():
        with open(Env.get()) as file:
            env = yaml.load(file,Loader = yaml.FullLoader)
        return env['colors']

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

    def df_columns():
        col = Lang.use()
        return col['df_columns']

    def urgency():
        col = Lang.use()
        return col['urgency']

ROOTDIR = 'src'
DATA_PATH = Path.get('data')

ERR_MSG = Lang.errors()
COLNAME = Lang.df_columns()
URGENCY = Lang.urgency()

COLORS = Env.mapcolors()