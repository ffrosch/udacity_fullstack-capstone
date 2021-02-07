import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()