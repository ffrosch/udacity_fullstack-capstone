from flask import Blueprint
from .routes import TestAPI, TourAPI

api = Blueprint('api', __name__)

test_view = TestAPI.as_view('api')
api.add_url_rule('/', view_func=test_view)

