from fetchFeed import fetchBundle
import datetime, pytz
header = ["empty_slots", "free_bikes", "timestamp"]
tz_hel = pytz.timezone("Europe/Helsinki")
needed_headers = ("id", "bikesAvailable", "spacesAvailable", "allowDropoff",
                    "isFloatingBike", "state", "realTimeData")
def genStatus(URL_STATUS):
    bundle = fetchBundle(URL_STATUS)
    stationsInfo = list()
    if type(bundle) is dict:
        try:
            stationsInfo = bundle['stations']
        except:
            stationsInfo

    if stationsInfo:
        date_time = datetime.datetime.now(tz_hel).strftime('%Y-%m-%d %H:%M:%S').split(' ')
        data = list()
        for station in stationsInfo:
            data.clear()
            for field in needed_headers:
                try:
                    data.append(station[field])
                except:
                    data.append( "NULL")
            #appending date and time to seperate fields
            data.append(date_time[0])
            data.append(date_time[1])
            #appending current data flag
            data.append(1)
            yield data

    else:
        return stationsInfo
def fetchCompanyInfo():
    pass

def fetchLocInfo():
    pass
