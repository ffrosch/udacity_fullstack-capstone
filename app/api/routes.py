from flask import jsonify
# from flask import current_app as app
from flask.views import MethodView


class TestAPI(MethodView):
    decorators = []

    def get(self):
        return 'Hello GET'

    def post(self):
        return jsonify(success=True, message='Hello POST')
