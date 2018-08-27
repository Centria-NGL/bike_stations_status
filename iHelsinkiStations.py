import pypyodbc, time, logging, threading
from HelsinkiStations import genStatus

REQ_INTERVALS = 15
logging.basicConfig(filename= 'HELSINKI_StationsStatus.log', level = logging.DEBUG,
                    format = '(%(asctime)s) %(levelname)s : %(message)s',
                    filemode='w')

db_host = 'YOUSERVERADDRESS'
db_name = 'DBNAME'
db_user = 'USERNAME'
db_password = 'PASSWORD'
URL_HELSINKI_STATUS = "https://api.digitransit.fi/routing/v1/routers/hsl/bike_rental"

connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'

SQLCommand_StationsStatus = ('INSERT INTO HELSINKI_STATIONS_STATUS_LIVE '
                            '(STATION_ID, NUM_BIKES_AVAILABLE, NUM_DOCKS_AVAILABLE,'
                            'ALLOWED_DROP_OFF, IS_FLOATING_BIKE, STATION_STATE, IS_REAL_TIME, '
                            'LAST_REPORTED_DATE, LAST_REPORTED_TIME, IS_CURRENT) '
                            ' VALUES (?,?,?,?,?,?,?,?,?,?)')

set_current_zero_command_sql = ("UPDATE HELSINKI_STATIONS_STATUS_LIVE "
                               "SET IS_CURRENT = ? "
                               " WHERE LAST_REPORTED_TIME = ?")

retrieve_last_updated_time = "SELECT TOP 1 * FROM [HELSINKI_STATIONS_STATUS_LIVE] ORDER BY ROWID DESC"



def insertData(SQLCommand):
    logging.info("initiating connection")
    LAST_REPORTED_TIME = list()
    connection = pypyodbc.connect(connection_string)
    cursor = connection.cursor()

    cursor.execute(retrieve_last_updated_time)
    row = cursor.fetchone()

    if row:
        LAST_REPORTED_TIME.append(0)
        LAST_REPORTED_TIME.append(row[-2])
        cursor.execute(set_current_zero_command_sql, LAST_REPORTED_TIME)
        connection.commit()
    for entry in genStatus(URL_HELSINKI_STATUS):
        cursor.execute(SQLCommand, entry)
    connection.commit()
    connection.close()

def collectNonStop():
    threading.Timer(REQ_INTERVALS, collectNonStop).start()
    logging.info("STARTING Helsinki DATA COLLECTION")
    try:
        insertData(SQLCommand_StationsStatus)
    except Exception as e:
        logging.exception("failed to insert Helsinki status data into database")
        time.sleep(11)
        collectNonStop()


collectNonStop()
