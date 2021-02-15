from flask import Blueprint
from .routes import APIHome, ActivityAPIModerator, ActivityAPIPublic, TourAPI

api = Blueprint('api', __name__)

from . import errors  # nopep8

home_view = APIHome.as_view('home')
api.add_url_rule('/', view_func=home_view)

tour_view = TourAPI.as_view('tours')
api.add_url_rule('/tours/',
                 defaults={'tour_id': None},
                 view_func=tour_view,
                 methods=['GET', 'POST'])
api.add_url_rule('/tours/<int:tour_id>',
                 view_func=tour_view,
                 methods=['GET', 'PATCH', 'DELETE'])

activity_view_public = ActivityAPIPublic.as_view('activity_public')
activity_view_moderator = ActivityAPIModerator.as_view('activity_moderator')
api.add_url_rule('/activities/',
                 defaults={'activity_id': None},
                 view_func=activity_view_public,
                 methods=['GET'])
api.add_url_rule('/activities/',
                 defaults={'activity_id': None},
                 view_func=activity_view_moderator,
                 methods=['POST'])
api.add_url_rule('/activities/<int:activity_id>',
                 view_func=activity_view_public,
                 methods=['GET'])
api.add_url_rule('/activities/<int:activity_id>',
                 view_func=activity_view_moderator,
                 methods=['PATCH', 'DELETE'])
