import folium
from src.conf import COLNAME, COLORS, ERR_MSG, URGENCY
from src.utils import Utils

class Export:
    def to_html(toPlot,polygon):
        urgencyValues = toPlot[COLNAME['urgency']].unique().tolist()
        flag = True
        for urgency in urgencyValues:
            traceColor = COLORS[Utils.get_key_by_value(URGENCY,urgency)]
            traceToPlot = toPlot[toPlot[COLNAME['urgency']] == urgency]
            htmlPoint = f'<span style="height: 10px;width: 10px;background-color: {traceColor};border-radius: 100%;display: inline-block;"></span>'
            name = htmlPoint + ' ' + urgency
            if(traceColor == False):
                raise Exception(ERR_MSG['key_not_found'])
            if(flag):
                map = traceToPlot.explore(
                    popup = True,
                    name = name,
                    color = traceColor
                )
                flag = False
            else:
                traceToPlot.explore(m = map,
                    popup = True,
                    name = name,
                    color = traceColor
                )
            
        folium.LayerControl(collapsed = False).add_to(map)  # use folium to add layer control
        outfp = r"tripMap.html"
        map.save(outfp)