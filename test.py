#from src.testclass import *

from src.FlowStudy import flow


# flow(all = True,day = 8, hourRange= '00-12')
# for year in range(2018,2022):
#     flow(False,year,day = 8, hourRange= '00-12')

flow(all = True)
for year in range(2018,2022):
    flow(False,year)
