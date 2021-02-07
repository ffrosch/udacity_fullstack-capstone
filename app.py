from flask import Flask

from .models import setup_db


def create_app():
    app = Flask(__name__)
    setup_db(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app
