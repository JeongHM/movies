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
    param = dict(request.args) if request.args else None
    body = request.get_json()

    service = MoviesService(param=param, body=body)

    if request.method == "GET":
        result, code, message = service.get_all_movies()

        if not result:
            return RESPONSE_CODE[code], None, message, 400

        return RESPONSE_CODE[code], message, None, 200

    elif request.method == "POST":
        result, code, message = service.post_movie()

        if not result:
            return RESPONSE_CODE[code], None, message, 400

        return RESPONSE_CODE["CREATED"], None, None, 201

    elif request.method == "PUT":
        pass

    else:
        pass


@movies_blueprint.route(rule="/<movie_id>",
                        methods=["GET"],
                        endpoint="get_specific_movie")
@response_object_formatting
def get_specific_movie(movie_id: str):
    pass