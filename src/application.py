from flask import Flask


def create_app():
    app = Flask(import_name=__name__)

    return app


application = create_app()


if __name__ == '__main__':
    application.run(host="0.0.0.0", port="5050", debug=False)