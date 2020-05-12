import datetime
import time

import psycopg2
from wac import config

# Note: Using raw SQL here for "fun", but really should use an ORM


def connect():
    """Connect to the SQL database."""
    return psycopg2.connect(config.POSTGRES_ENDPOINT)


def setup_table(sql_conn):
    """Set up the table if it doesn't already exist.

    :param sql_conn: SQL Connection
    """
    # Run as a single transaction
    # See: https://www.psycopg.org/docs/usage.html#with-statement
    with sql_conn:
        with sql_conn.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS measurements ("
                "id SERIAL PRIMARY KEY, "
                "date TIMESTAMP, "
                "url VARCHAR(255), "
                "status_code SMALLINT, "
                "error VARCHAR(255),"
                "response_time NUMERIC);"
            )


def insert_data(
    cursor,
    url: str,
    status_code: int = 0,
    error: str = "",
    response_time: float = -1,
    timestamp: float = None,
):
    """Insert data into the table

    :param cursor: SQL Cursor
    :param url: URL monitored
    :param status_code: HTTP Status Code returned
    :param error: Optional error message
    :param response_time: Seconds until server responded
    """
    timestamp = timestamp or time.time()  # Use current time if none provided
    # Message sends timestamp, but need datetime for SQL
    date = datetime.datetime.fromtimestamp(timestamp)
    cursor.execute(
        "INSERT INTO measurements (url, status_code, error, response_time, date) "
        "VALUES (%s, %s, %s, %s, %s)",
        (url, status_code, error, response_time, date,),
    )
