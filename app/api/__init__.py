from flask import Blueprint, jsonify
from .routes import APIHome, TourAPI, ActivityAPI

api = Blueprint('api', __name__)

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

activity_view = ActivityAPI.as_view('activity')
api.add_url_rule('/activity/',
                 defaults={'activity_id': None},
                 view_func=activity_view,
                 methods=['GET', 'POST'])
api.add_url_rule('/activity/<int:activity_id>',
                 view_func=activity_view,
                 methods=['GET', 'PATCH', 'DELETE'])


######################
### Error Handlers ###
######################

# Errors 404 and 500 are handled by the main flask app
# They cannot reliably be handled by blueprints
# See flask.blueprint docs for further information

@api.errorhandler(400)
def _handle_400_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@api.errorhandler(401)
def _handle_401_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401

@api.errorhandler(403)
def _handle_403_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403

@api.errorhandler(405)
def _handle_405_error(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "not allowed"
                }), 405

@api.errorhandler(422)
def _handle_422_error(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
