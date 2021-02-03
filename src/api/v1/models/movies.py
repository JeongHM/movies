import sqlite3
from flask import current_app


from src.api.v1.models import connection


class MoviesModel(object):
    def __init__(self):
        self._conn = connection()

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

    def select_all_movies(self, columns: list = None) -> list:
        """
        select all data in movie table
            MoviesModel().select_all_movies()
        :param columns: column names
        :return:
        """

        cols = ", ".join(columns) if columns else "*"
        sql = f"SELECT {cols} FROM movies"

        with self._conn as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            query = cursor.execute(sql)

            rows = query.fetchall()

        return rows

    def insert_movie(self, movie: dict):
        """
        insert data into movie table
            MoviesModel().insert_movie(body={})
        :param movie: movie object
        :return:
        """
        sql = "INSERT INTO movies (name, genre, grade, release_at, views) " \
              "VALUES (:name, :genre, :grade, :release_at, :views)"

        with self._conn as con:
            cursor = con.cursor()
            cursor.execute(sql, movie)
            last_id = cursor.lastrowid

            con.commit()

        return last_id

    def update_movies(self, movies: list):
        """
        update data in movie table
        :param movies: movie object list
        :return:
        """
        sql = "UPDATE movies " \
              "SET genre = :genre, grade = :grade, release_at = " \
              ":release_at, views = :views " \
              "WHERE name = :name;"

        with self._conn as con:
            cursor = con.cursor()

            for movie in movies:
                cursor.execute(sql, movie)

            con.commit()

    def delete_movies(self):
        """
        delete all data in movie table
        :return:
        """
        sql = "DELETE FROM movies"

        with self._conn as con:
            cursor = con.cursor()
            cursor.execute(sql)

            con.commit()

    def select_movie_by_id(self, param: dict) -> list:
        """
        select movie data by id
        :param param: id parameter ({id: id})
        :return:
        """
        sql = "SELECT * FROM movies WHERE movies.id = :movie_id"

        with self._conn as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()

            query = cursor.execute(sql, param)
            row = query.fetchone()

        return row

    def select_movie_by_name(self, names: list) -> list or object:
        """
        select movie id by name
        :param names: movie name list
        :return:
        """

        sql = "SELECT id FROM movies WHERE movies.name = :movie_name"
        movie_ids = list()

        with self._conn as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()

            for name in names:
                cursor.execute(sql, {"movie_name": name})
                movie = cursor.fetchone()

                if movie is None:
                    raise ValueError("NoneType Error: movie.name")
                movie_ids.append(dict(movie).get("id"))

        return movie_ids
