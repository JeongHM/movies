import sqlite3
from flask import current_app


from src.api.v1.models import connection


class MoviesModel(object):
    def __init__(self, parameters: list or dict = None):
        self._conn = connection()
        self._parameters = parameters

    def init_table(self) -> None:
        """
        create table
            MoviesModel().init_table()
        :return: None
        """
        with self._conn as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS movies (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        VARCHAR(255) ,
                genre       VARCHAR(50) NOT NULL,
                grade       INTEGER NOT NULL,
                views       INTEGER DEFAULT 0,
                release_at  TEXT NOT NULL,
                created_at  DEFAULT CURRENT_TIMESTAMP NOT NULL,
                UNIQUE(name)
            );""")
            con.commit()


