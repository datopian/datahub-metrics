import psycopg2
import envVariables
from urllib.parse import urlparse


def setUpPsql():
    global cursor, URI
    URI = envVariables.URI
    cursor = getConnectionCursorFromURI()


def getConnectionCursorFromURI():
    result = urlparse(URI)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    connection = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )
    cursor = connection.cursor()
    return cursor


def getCountOfTotalUsers():
    cursor.execute("""SELECT count(*) FROM users;""")
    return getQueryResultFromCursor(cursor)


def getCountOfAllDatasets():
    cursor.execute("""SELECT count(*) FROM dataset;""")
    return getQueryResultFromCursor(cursor)


# Bear in mind that we don't write this value into the sheet's cell but we must
# subtract it from another value
def getCountOfUnlistedDatasets():
    cursor.execute("""
        SELECT count(*) FROM dataset WHERE spec LIKE '%"findability": "unlisted"%' AND
        (owner='b6c7c7180404aeb2863e592a9a72deb9' OR owner ='81429cbbddcfb180f54c142fac32f83b'
        OR owner='a08d3588fbae0355042537595c65819d' OR owner='90998f7f90e086bd5fc7c9075dfda43b'
        OR owner='test' OR owner='examples' OR owner='core');"""
    )
    return getQueryResultFromCursor(cursor)


def getCountOfPrivateDatasets():
    cursor.execute("""SELECT count(*) FROM dataset WHERE spec LIKE '%"findability": "private"%';""")
    return getQueryResultFromCursor(cursor)


# Bear in mind that we don't write this value into the sheet's cell but we must subtract it from another value
def getCountOfPrivateDatasetsExtractingOur():
    cursor.execute(
        """SELECT count(*) FROM dataset WHERE spec LIKE '%"findability": "private"%' AND
        (owner='b6c7c7180404aeb2863e592a9a72deb9' OR owner='81429cbbddcfb180f54c142fac32f83b'
        OR owner='a08d3588fbae0355042537595c65819d' OR owner='90998f7f90e086bd5fc7c9075dfda43b'
        OR owner='d451723ceddb251c471e563af49f38de' OR owner='test' OR owner='examples'
        OR owner='core');"""
    )
    return getQueryResultFromCursor(cursor)


def getCountOfPublishedDatasets():
    cursor.execute(
        """SELECT count(*) FROM dataset WHERE spec LIKE '%"findability": "published"%';"""
    )
    return getQueryResultFromCursor(cursor)


def getCountOfAllPushRequests(currentDateTimestamp):
    cursor.execute(
        """SELECT count(*) FROM dataset_revision WHERE created_at::text LIKE """
        + "'" + currentDateTimestamp + "%'" + ";"
    )
    return getQueryResultFromCursor(cursor)


def getCountOfPushRequestsExcludingUs(currentDateTimestamp):
    timestampLikeString = "'" + currentDateTimestamp + "%'"
    selectStatement = """
        SELECT count(*) FROM dataset_revision WHERE created_at::text LIKE """ + timestampLikeString + """
        AND NOT (dataset_id LIKE 'cd511289b5773fff5e7efe328846eef3%' OR dataset_id LIKE 'b6c7c7180404aeb2863e592a9a72deb9%'
        OR dataset_id LIKE '81429cbbddcfb180f54c142fac32f83b%' OR dataset_id LIKE 'a08d3588fbae0355042537595c65819d%'
        OR dataset_id LIKE '90998f7f90e086bd5fc7c9075dfda43b%' OR dataset_id LIKE 'd451723ceddb251c471e563af49f38de%');
    """
    cursor.execute(selectStatement)
    return getQueryResultFromCursor(cursor)


def getCountOfNewUsersWhoPublishedDatasetBetweenDates(startDate, endDate):
    selectStatement = """
        SELECT dataset.owner, count(*) FROM users INNER JOIN dataset on users.id = dataset.owner
        WHERE users.join_date::date BETWEEN date '""" + startDate + """' AND date '""" + endDate + """'
        GROUP BY dataset.owner HAVING count(*) > 0;
    """
    cursor.execute(selectStatement)
    return getNumberOfRowsInQueryResult(cursor)


def getCountOfNewUsersWhoPublishedMoreThanOneDatasetBetweenDates(startDate, endDate):
    selectStatement = """
        SELECT dataset.owner, count(*) FROM users INNER JOIN dataset on users.id = dataset.owner
        WHERE users.join_date::date BETWEEN date '""" + startDate + """' AND date '""" + endDate + """'
        GROUP BY dataset.owner HAVING COUNT(*) > 1;
    """
    cursor.execute(selectStatement)
    return getNumberOfRowsInQueryResult(cursor)


def getCountOfNewDatasetsBetweenDates(startDate, endDate):
    selectStatement = """
        SELECT count(*) FROM dataset WHERE created_at::date BETWEEN date '""" + startDate + """' AND date '""" + endDate + """';
    """
    cursor.execute(selectStatement)
    return getQueryResultFromCursor(cursor)


def getQueryResultFromCursor(cursor):
    rows = cursor.fetchone()
    return rows[0]


def getNumberOfRowsInQueryResult(cursor):
    rows = cursor.fetchall()
    return len(rows)


setUpPsql()
