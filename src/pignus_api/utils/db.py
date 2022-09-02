"""Utils - DB
Database handler.

"""
import os

import pymysql.cursors

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

# End File: pignus/src/pignus_api/utils/db.py
