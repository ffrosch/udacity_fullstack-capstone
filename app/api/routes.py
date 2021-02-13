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


def user_status(f):
    def decorator(*args, **kwargs):
        user = {}
        token = None  # TODO: implement get_token_auth_header
        payload = None  # TODO: implement get_payload
        auth = False  # TODO: implement check_auth() -> True/False
        if auth:
            user['auth'] = True
            user['permissions'] = payload['permissions']
            user['id'] = payload['user_id']
        else:
            user['auth'] = False
            user['permissions'] = []
            user['id'] = None
        return f(*args, user=user, **kwargs)
    return decorator


def get_permissions():
    # TODO: Implement
    pass


class TestAPI(MethodView):
    decorators = [test('Tested')]

    def get(self, x):
        return f'Hello GET: {x}'

    def post(self):
        return jsonify(success=True, message='Hello POST')


class TourAPI(MethodView):
    decorators = [user_status]

    def get(self, tour_id, user):
        # GET All
        if tour_id is None:
            if user['auth']:
                if 'admin' in user['permissions']:
                    tours = Tour.query.all()
                else:
                    tours = Tour.query.filter(or_(
                        Tour.accesslevel.has(name='Public'),
                        Tour.user_id == user['id'])
                    ).all()
            else:
                tours = Tour.query.filter(
                    Tour.accesslevel.has(name='Public')
                ).all()
        # GET <int:tour_id>
        else:
            tour = Tour.query.filter(Tour.id == tour_id).first()
            if tour is None:
                abort(404)
            if tour.accesslevel.name == 'Private':
                if not user['auth']:
                    abort(401)
                if tour.user_id != user['id']:
                    abort(403)
            tours = [tour]

        data = {'success': True,
                'tours': [tour.as_geojson() for tour in tours]}

        return jsonify(data), 200

    def patch(self, tour_id, user):
        pass

    def delete(self, tour_id, user):
        pass
