"""Utils - DB
Database handler.

"""
import os

import pymysql.cursors
import mysql.connector
from mysql.connector import Error as MySqlError

from pignus_shared.utils import log


PIGNUS_DB_HOST = os.environ.get("PIGNUS_DB_HOST")
PIGNUS_DB_PORT = int(os.environ.get("PIGNUS_DB_PORT"))
PIGNUS_DB_NAME = os.environ.get("PIGNUS_DB_NAME")
PIGNUS_DB_USER = os.environ.get("PIGNUS_DB_USER")
PIGNUS_DB_PASS = os.environ.get("PIGNUS_DB_PASS")


def connect():
    # Connect to the database
    connection = pymysql.connect(
        host=PIGNUS_DB_HOST,
        port=PIGNUS_DB_PORT,
        user=PIGNUS_DB_USER,
        password=PIGNUS_DB_PASS,
        database=PIGNUS_DB_NAME)

    log.info("Generating database connection")
    return {
        "conn": connection,
        "cursor": connection.cursor()
    }


def connect_no_db(server: dict):
    """Connect to MySql server, without specifying a database, and get a cursor object."""
    try:
        connection = mysql.connector.connect(
            host=PIGNUS_DB_HOST,
            user=PIGNUS_DB_USER,
            password=PIGNUS_DB_PASS)
        if connection.is_connected():
            db_info = connection.get_server_info()
            log.debug(db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            log.debug(record)
        return {
            "conn": connection,
            "cursor": cursor,
        }
    except MySqlError as e:
        log.error("Error while connecting to MySQL: %s" % e, exception=e)
        exit(1)


def create_mysql_database(conn, cursor, db_name: str):
    """Create the MySQL database."""
    sql = """CREATE DATABASE IF NOT EXISTS %s""" % db_name
    cursor.execute(sql)
    log.info('Created database: %s' % db_name)
    return True

# End File: pignus/src/pignus_api/utils/db.py
