import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')

    from app.view import view
    app.register_blueprint(view, url_prefix='')

    # These errors can't be handled in blueprints
    # because the app wouldn't know which blueprint to use
    @app.errorhandler(404)
    def _handle_404_api_error(e):
        if request.path.startswith('/api'):
            return jsonify({
                "success": False,
                "error": 404,
                "message": "not found"
            }), 404
        else:
            return e

    @app.errorhandler(405)
    def _handle_405_api_error(e):
        if request.path.startswith('/api'):
            return jsonify({
                "success": False,
                "error": 405,
                "message": "not allowed"
            }), 405
        else:
            return e

    return app


from app import models  # nopep8
