import logging
from flask import Flask, request, current_app
from flask_cors import CORS
from logging.handlers import RotatingFileHandler

from src.api.v1.models.movies import MoviesModel
from src.api.common.constants import CONSTANTS
from src.api.common.response_cods import RESPONSE_CODE
from src.api.common.decorators import response_object_formatting


def create_app():
    """
    Setting app config, logging, cors ..
    :return: Flask()
    """
    # Set Flask App
    app = Flask(import_name=__name__)

    # Set Logging
    logger = logging.getLogger(name=__name__)
    logger.setLevel(level=logging.INFO)
    logger_format = "[%(asctime)s] %(pathname)s:%(lineno)d  %(message)s"
    logger_formatter = logging.Formatter(fmt=logger_format)
    logger_handler = RotatingFileHandler(filename="application.log",
                                         mode="a",
                                         maxBytes=1024 * 1024 * 3,
                                         backupCount=3,
                                         encoding="utf-8")
    logger_handler.setFormatter(fmt=logger_formatter)
    logger.addHandler(hdlr=logger_handler)

    app.logger.addHandler(hdlr=logger_handler)
    app.logger.setLevel(level=logging.INFO)

    # Set Blueprint
    from src.api.v1.controllers.movies import movies_blueprint
    app.register_blueprint(blueprint=movies_blueprint,
                           url_prefix=CONSTANTS["V1_MOVIE_API"])

    # Set CORS
    CORS(app=app)

    # Create table
    MoviesModel().init_table()

    return app


application = create_app()


@application.before_request
def before_request():
    method = request.method
    url = request.url
    params = request.args if request.args else None
    body = request.json if request.json else None

    current_app.logger.info(f'[{method}] {url} params: {params} body: {body}')


@application.errorhandler(404)
@response_object_formatting
def not_found_error(e):
    return RESPONSE_CODE["NOT_FOUND"], None, e, 404


if __name__ == '__main__':
    application.run(host="0.0.0.0", port="5050", debug=False)