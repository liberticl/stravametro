#from .classes.conf import Env, Path, Lang
from ast import Str
from .classes.strava import Strava
from .classes.filter import byTime

###### CONF ##########
# # Environment
# print(Env.get())
# print(Env.lang())
# print(Env.mapcolors())

# # Path
# print(Path.get('lang'))
# print(Path.get_names('lang'))

# # Lang
# print(Lang.use())
# print(Lang.errors())
# print(Lang.df_columns())
# print(Lang.urgency())


###### GOBAPI ############
# print(GobApi.get_all_communes_in_region("valparaiso"))

data = Strava.get_csv_data('/home/francisco/Andes Chile ONG/stravametro/src/lovasquez/2021')
byTime.hour_range(data,'03-07',7)