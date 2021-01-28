import sqlite3
from flask import current_app


from src.api.v1.models import connection


class MoviesService(object):
    def __init__(self, param: dict = None, body: dict = None) -> None:
        """
        Set request parameter or body
            class_name = MoviesServices(param=param, body=body)
        :param param: Request parameter
        :param body: Request body
        """
        self._param = param
        self._body = body
        self._connection = connection()

    def get_all_movies(self) -> (bool, str, str or list):
        """
        get all movies (select all movie object in database)
            MoviesServices().get_all_movies()
        :return: (bool, str or list[dict, dict, ...])
        """
        try:
            sql = "SELECT * FROM movies"

            with self._connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query = cursor.execute(sql)

                items = {"movies": [dict(row) for row in query.fetchall()]}

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e

        return True, "SUCCESS", items

    def post_movie(self) -> (bool, str, str or list):
        """
        create movie object (insert object to database)
            MoviesServices().post_movie()
        :return: (bool, str)
        """
        try:
            sql = "INSERT INTO movies (name, genre, grade, release_at, views) " \
                  "VALUES (?, ?, ?, ?, ?)"
            parameters = self._body.values()

            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute(sql,
                               tuple(parameters))

                conn.commit()
        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e

        return True, "SUCCESS", None

    def put_movie(self) -> (bool, str):
        """
        update movie object (update object to database)
            MoviesServices().put_movie()
        :return: (bool, str)
        """
        try:
            pass

        except Exception as e:
            current_app.logger.error(e)
            return False, None

        return True, True

    def delete_movie(self) -> (bool, str):
        """
        delete movie object (delete object to database)
            MoviesServices().delete_movie()
        :return: (bool, str)
        """
        try:
            pass

        except Exception as e:
            current_app.logger.error(e)
            return False, None

        return True, True

    def get_specific_movie(self) -> (bool, str):
        """
        get specific movie object (select specific movie object in database)
            MoviesServices().get_specific_movie()
        :return: (bool, str)
        """
        try:
            sql = "SELECT * FROM movies WHERE id = ?"
            parameter = self._param.get("movie_id")

            with self._connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query = cursor.execute(sql,
                                       parameter)

                item = dict(query.fetchone())

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e

        return True, "SUCCESS", item
