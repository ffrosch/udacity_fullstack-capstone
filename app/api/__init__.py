from flask import Blueprint
from .routes import TestAPI, TourAPI

api = Blueprint('api', __name__)

test_view = TestAPI.as_view('api')
api.add_url_rule('/', view_func=test_view)

tour_view = TourAPI.as_view('tours')
api.add_url_rule('/tours/',
                 defaults={'tour_id': None},
                 view_func=tour_view,
                 methods=['GET'])
api.add_url_rule('/tours/<int:tour_id>',
                 view_func=tour_view,
                 methods=['GET', 'PATCH', 'DELETE'])
