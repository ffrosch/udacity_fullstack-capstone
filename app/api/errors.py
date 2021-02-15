from flask import jsonify

from . import api
from .auth import AuthError

######################
#   Error Handlers   #
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


@api.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
