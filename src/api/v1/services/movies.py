import sqlite3
from flask import current_app, request

from src.api.v1.models.movies import MoviesModel
from src.api.v1.validators.movies import MovieSchema


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

    def get_all_movies(self) -> (bool, str, str or list, int):
        """
        get all movies (select all movie object in database)
            MoviesServices().get_all_movies()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            rows = MoviesModel().select_all_movies()

            if not rows:
                return None, "NO_CONTENT", None, None, 204

            items = {"movies": [dict(row) for row in rows]}

            links = [
                {
                    "rel": "self",
                    "href": request.url + "/" + str(dict(row).get("id"))
                } for row in rows
            ]

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, None, 400

        return True, "SUCCESS", items, links, 200

    def post_movie(self) -> (bool, str, str or list, int):
        """
        create movie object (insert object to database)
            MoviesServices().post_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            item = {}

            error = MovieSchema().validate(data=self._body)
            if error:
                raise ValueError("required: Missing data for required field.")

            last_id = MoviesModel().insert_movie(movie=self._body)

            links = [
                {
                    "rel": "self",
                    "href": request.url + "/" + str(last_id)
                }
            ]

        except sqlite3.IntegrityError as e:
            current_app.logger.error(e)
            return False, "CONFLICT", e, None, 409

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, None, 400

        return True, "CREATED", item, links, 201

    def put_movie(self) -> (bool, str, str or list, int):
        """
        update movie object (update object to database)
            MoviesServices().put_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:

            error = MovieSchema(many=True).validate(data=self._body["movies"])

            if error:
                raise ValueError("required: Missing data for required field.")

            movies = self._body["movies"]

            movie_names = [movie.get("name") for movie in movies]

            if len(movie_names) != len(set(movie_names)):
                raise KeyError('Duplicate Key Error: movie.name')

            movie_ids = MoviesModel().select_movie_by_name(names=movie_names)

            MoviesModel().update_movies(movies=movies)

            links = [
                {
                    "rel": "self",
                    "href": request.url + "/" + str(movie_id)
                } for movie_id in movie_ids
            ]

        except KeyError as e:
            current_app.logger.error(e)
            return False, "CONFLICT", e, None, 409

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, None, 400

        return True, "SUCCESS", None, links, 200

    def delete_movie(self) -> (bool, str, str or list, int):
        """
        delete movie object (delete object to database)
            MoviesServices().delete_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:
            MoviesModel().delete_movies()

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, None, 400

        return True, "NO_CONTENT", None, None, 204

    def get_specific_movie(self) -> (bool, str, str or list, int):
        """
        get specific movie object (select specific movie object in database)
            MoviesServices().get_specific_movie()
        :return: result(bool), code(str), error or result object, status_code
        """
        try:

            row = MoviesModel().select_movie_by_id(param=self._param)

            if not row:
                return None, "NO_CONTENT", None, None, 204

            item = {"movie": dict(row)}

        except Exception as e:
            current_app.logger.error(e)
            return False, "BAD_REQUEST", e, None, 400

        return True, "SUCCESS", item, None, 200
