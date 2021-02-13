from flask import jsonify, abort, request
from flask.views import MethodView
from sqlalchemy import and_, or_
from functools import wraps

from app.models import Tour, Accesslevel, Activity


def test(arg=''):
    def test_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(arg, *args, **kwargs)
        return wrapper
    return test_decorator


class TestAPI(MethodView):
    decorators = [test('Tested')]

    def get(self, x):
        return f'Hello GET: {x}'

    def post(self):
        return jsonify(success=True, message='Hello POST')
