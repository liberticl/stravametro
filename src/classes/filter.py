
class byTime:
    # use when extract data hourly from Strava Metroview
    def hour_range(data, hourRange:str, day = None):
        if(day):
            day = str(day)
            if(len(day) == 1):
                day = '0' + day
            data = data[data['hour'].str.contains('-' + day + 'T')].reset_index()
        
        timeRange = hourRange.split('-')
        hours = list(range(int(timeRange[0]),int(timeRange[1]) + 1))
        hours = ['T0' + hour for hour in [str(hr) for hr in hours]]
        hours = '|'.join(hours)
        data = data[data['hour'].str.contains(hours)].reset_index()

        return data