from flask import Flask
from flask_cors import CORS

from src.api.v1.models.movies import MoviesModel
from src.api.common.constants import CONSTANTS


def create_app():
    """
    Setting app config, logging, cors ..
    :return: Flask()
    """
    # Set Flask App
    app = Flask(import_name=__name__)

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


if __name__ == '__main__':
    application.run(host="0.0.0.0", port="5050", debug=False)