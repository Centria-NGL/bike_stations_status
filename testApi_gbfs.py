system_information = "https://gbfs.citibikenyc.com/gbfs/en/system_information.json"
station_information = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
system_alerts = "https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json"
system_regions = "https://gbfs.citibikenyc.com/gbfs/en/system_regions.json"
station_status = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
SEP =";"

import threading, pytz, datetime
from fetchFeed import fetchBundle
from parse_system_information import parseSystemInformation
# from parse_stations import parseStations
import StationsStatus

tz_nyc = pytz.timezone("America/New_York")


hdrsStatus = ["station_id", "num_bikes_available", "num_ebikes_available" , "num_bikes_disabled",
                "num_docks_available", "num_docks_disabled", "is_installed",
                 "is_renting", "is_returning", "last_reported"]

hdrsStations = ["station_id", "name", "short_name", "lat", "lon", "region_id",
                "rental_methods", "capacity"]


def out_stream(txt, fname):
    with open(fname, 'a') as f:
        f.write(txt)


def fetchStatus():
    response = list()
    for entry in StationsStatus.fetchStatus():
        response.append(entry)
    for v in response:
        print(v)

fetchStatus()
