import sqlite3
from flask import current_app, request


from src.api.v1.models import connection


class MoviesService(object):
    def __init__(self, param: dict = None, body: dict or list = None) -> None:
        """
        Set request parameter or body
            class_name = MoviesServices(param=param, body=body)
        :param param: Request parameter
        :param body: Request body
        """
        self._param = param
        self._body = body
        self._connection = connection()

    def get_all_movies(self) -> (bool, str, str or list, int):
        """
        get all movies (select all movie object in database)
            MoviesServices().get_all_movies()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            sql = "SELECT * FROM movies"
            items = {"movies": None}

            with self._connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query = cursor.execute(sql)

                movies = list()

                for row in query.fetchall():
                    movie = dict(row)
                    movie["link"] = {
                        "rel": "self",
                        "href": request.url + "/" + str(movie.get("id"))
                    }

                    movies.append(movie)
                items["movies"] = movies

                if not items["movies"]:
                    return None, "NO_CONTENT", None, 204

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, 400

        return True, "SUCCESS", items, 200

    def post_movie(self) -> (bool, str, str or list, int):
        """
        create movie object (insert object to database)
            MoviesServices().post_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            sql = "INSERT INTO movies (name, genre, grade, release_at, views) " \
                  "VALUES (:name, :genre, :grade, :release_at, :views)"

            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute(sql, self._body)

                item = {
                    "link": {
                        "rel": "self",
                        "href": request.url + "/" + str(cursor.lastrowid)
                    }
                }
                conn.commit()

        except sqlite3.IntegrityError as e:
            current_app.logger.error(e)
            return False, "CONFLICT", e, 409

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, 400

        return True, "SUCCESS", item, 200

    def put_movie(self) -> (bool, str, str or list, int):
        """
        update movie object (update object to database)
            MoviesServices().put_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            sql = "UPDATE movies " \
                  "SET genre = :genre, grade = :grade, release_at = " \
                  ":release_at, views = :views " \
                  "WHERE name = :name;"

            movies = self._body["movies"]

            movie_names = [movie.get("name") for movie in movies]

            if len(movie_names) != len(set(movie_names)):
                raise KeyError('Duplicate Key Error: movie.name')

            with self._connection as conn:
                cursor = conn.cursor()

                for movie in movies:
                    cursor.execute(sql, movie)

            conn.commit()

        except KeyError as e:
            current_app.logger.error(e)
            return False, "CONFLICT", e, 409

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, 400

        return True, "SUCCESS", None, 200

    def delete_movie(self) -> (bool, str, str or list, int):
        """
        delete movie object (delete object to database)
            MoviesServices().delete_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            sql = "DELETE FROM movies"

            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                conn.commit()

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, 400

        return True, "SUCCESS", None, 200

    def get_specific_movie(self) -> (bool, str, str or list, int):
        """
        get specific movie object (select specific movie object in database)
            MoviesServices().get_specific_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            sql = "SELECT * FROM movies WHERE movies.id = :movie_id"

            with self._connection as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = cursor.execute(sql, self._param)
                row = query.fetchone()

                if not row:
                    return None, "NO_CONTENT", None, 204

                item = {"movie": dict(row)}

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, 400

        return True, "SUCCESS", item, 200
