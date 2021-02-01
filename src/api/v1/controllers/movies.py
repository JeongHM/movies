from flask import Blueprint, request

from src.api.v1.services.movies import MoviesService
from src.api.common.response_cods import RESPONSE_CODE
from src.api.common.decorators import response_object_formatting


movies_blueprint = Blueprint(name="movies", import_name=__name__)


@movies_blueprint.route(rule="",
                        methods=["GET", "POST", "PUT", "DELETE"],
                        endpoint="movies")
@response_object_formatting
def movies():
    result, code, message, status = None, None, None, None

    param = dict(request.args) if request.args else None
    body = request.get_json()

    service = MoviesService(param=param, body=body)

    if request.method == "GET":
        result, code, message, status = service.get_all_movies()

    elif request.method == "POST":
        result, code, message, status = service.post_movie()

    elif request.method == "PUT":
        result, code, message, status = service.put_movie()

    else:
        result, code, message, status = service.delete_movie()

    if not result:
        return RESPONSE_CODE[code], None, message, status

    return RESPONSE_CODE[code], message, None, status


@movies_blueprint.route(rule="/<int:movie_id>",
                        methods=["GET"],
                        endpoint="get_specific_movie")
@response_object_formatting
def get_specific_movie(movie_id: int):
    param = {"movie_id": movie_id}

    service = MoviesService(param=param)
    result, code, message, status = service.get_specific_movie()

    if not result:
        return RESPONSE_CODE[code], None, message, status

    return RESPONSE_CODE[code], message, None, status