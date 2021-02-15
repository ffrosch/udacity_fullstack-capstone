from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')

    from app.view import view
    app.register_blueprint(view, url_prefix='')

    # These errors can't be handled in blueprints
    # because the app wouldn't know which blueprint to use
    @app.errorhandler(404)
    def _handle_404_api_error(error):
        if request.path.startswith('/api'):
            return jsonify({
                "success": False,
                "error": 404,
                "message": "not found"
            }), 404
        else:
            return error

    @app.errorhandler(500)
    def _handle_500_api_error(error):
        if request.path.startswith('/api'):
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500
        else:
            return error

    return app


from app import models  # nopep8
