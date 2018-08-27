import pytz, datetime
from fetchFeed import fetchBundle
from parse_system_information import parseSystemInformation

URL_STATUS_NYC = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
SEP =";"
tz_nyc = pytz.timezone("America/New_York")
hdrsStatus = ["station_id", "num_bikes_available", "num_ebikes_available" , "num_bikes_disabled",
                "num_docks_available", "num_docks_disabled", "is_installed",
                 "is_renting", "is_returning", "last_reported"]

def fetchStatus(URL_STATUS=URL_STATUS_NYC):
    bundle = fetchBundle(URL_STATUS)
    if type(bundle) is dict:
        stationsInfo = bundle["data"]["stations"]
        date_time = datetime.datetime.now(tz_nyc).strftime('%Y-%m-%d %H:%M:%S').split(' ')
        data = list()
        for station in stationsInfo:
            data.clear()
            for header in hdrsStatus[:-1]:
                try:
                    data.append(station[header])
                except:
                    data.append( "NULL")
            data.append(date_time[0])
            data.append(date_time[1])
            data.append(1)
            yield data
