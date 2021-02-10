from flask import Blueprint
from .routes import TestAPI

api = Blueprint('api', __name__)
api.add_url_rule('/', view_func=TestAPI.as_view('api'))
