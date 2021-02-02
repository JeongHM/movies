import sqlite3

from src.api.common.constants import CONSTANTS


def connection():
    """
    get sqlite connection
    :return: sqlite3.connect()
    """
    return sqlite3.connect(database=CONSTANTS["DATABASE_PATH"])
