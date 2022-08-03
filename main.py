from src.FlowStudy import flow,cuantitative

flow(all = True)
for year in range(2019,2022):
    flow(False,year)

cuantitative()