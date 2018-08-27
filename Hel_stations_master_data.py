import csv
from fetchFeed import fetchBundle
URL_STATUS = "https://api.digitransit.fi/routing/v1/routers/hsl/bike_rental"
header = ("id", "name", "lat", "lon")

def ostream():
    with open("Hel_stations_Master.csv", 'w') as ofile:
        writer = csv.writer(ofile, delimiter=';')
        writer.writerow(header)
        for entry in genStations():
            writer.writerow(entry)

def genStations():
    bundle = fetchBundle(URL_STATUS)
    stationsInfo = list()
    if type(bundle) is dict:
        try:
            stationsInfo = bundle['stations']
        except:
            return stationsInfo
    if stationsInfo:
        data = list()
        for station in stationsInfo:
            data.clear()
            data.append(station['id'])
            data.append(station['name'])
            data.append(station['y'])
            data.append(station['x'])
            yield data

ostream()
