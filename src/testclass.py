from .classes.conf import Env, Path, Lang
from .classes.osm import 

###### CONF ##########
# Environment
print(Env.get())
print(Env.lang())
print(Env.mapcolors())

# Path
print(Path.get('lang'))
print(Path.get_names('lang'))

# Lang
print(Lang.use())
print(Lang.errors())
print(Lang.df_columns())
print(Lang.urgency())


###### DRAW ############
