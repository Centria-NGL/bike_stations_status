import pypyodbc, time, logging, threading
from StationsStatus import fetchStatus

REQ_INTERVALS = 15
logging.basicConfig(filename= 'log_StationsStatus.log', level = logging.DEBUG,
                    format = '(%(asctime)s) %(levelname)s : %(message)s',
                    filemode='w')

db_host = 'YOUSERVERADDRESS'
db_name = 'DBNAME'
db_user = 'USERNAME'
db_password = 'PASSWORD'


connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'

SQLCommand_StationsStatus = ("INSERT INTO STATIONS_STATUS_LIVE"
"(STATION_ID, NUM_BIKES_AVAILABLE, NUM_EBIKES_AVAILABLE, NUM_BIKES_DISABLED,"
"NUM_DOCKS_AVAILABLE, NUM_DOCKS_DISABLED, IS_INSTALLED, IS_RENTING, IS_RETURNING,"
"LAST_REPORTED_DATE, LAST_REPORTED_TIME, IS_CURRENT)"
"VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")


set_current_zero_command_sql = ("UPDATE STATIONS_STATUS_LIVE "
                               "SET IS_CURRENT = ? "
                               " WHERE LAST_REPORTED_TIME = ?")

retrieve_last_updated_time = "SELECT TOP 1 * FROM [STATIONS_STATUS_LIVE] ORDER BY ROWID DESC"

def insertData(SQLCommand):
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

    for entry in fetchStatus():
        cursor.execute(SQLCommand, entry)
        connection.commit()
    connection.close()

def collectNonStop():
    threading.Timer(REQ_INTERVALS, collectNonStop).start()
    logging.info("STARTING DATA COLLECTION")
    try:
        insertData(SQLCommand_StationsStatus)
    except Exception as e:
        logging.exception("failed to insert NY stations data into database")
        time.sleep(11)
        collectNonStop()
    else:
        logging.info("inserted NY stations status data")

collectNonStop()
