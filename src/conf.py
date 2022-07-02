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

class Lang:
    def __init__(self):
        self.lang = Env.lang()
        try: 
            for obj in os.scandir(ROOTDIR):
                if obj.is_dir() and 'lang' in obj.name:
                    self.dir = os.path.dirname(os.path.realpath(obj.path + os.sep + obj.name))
        except:
            raise Exception("lang directory does not exist!")

    def use():
        this = Lang()
        file = "/" + this.lang + ".yaml"
        with open(this.dir + file) as language:
            return yaml.load(language,Loader = yaml.FullLoader)

    def errors():
        messages = Lang.use()
        return messages['errors']

ROOTDIR = 'src'
ERR_MSG = Lang.errors()
