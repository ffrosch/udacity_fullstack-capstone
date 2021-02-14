import sys

from flask import jsonify, abort, request
from flask.views import MethodView
from sqlalchemy import and_, or_
from functools import wraps

from app.api.auth import user_status, verify_decode_jwt, get_token_auth_header
from app.models import Tour, Accesslevel, Activity


class APIHome(MethodView):
    msg = 'You are at /api/'
    def get(self):
        return f'Hello GET: </br></br>{self.msg}'

    def post(self):
        return jsonify(success=True, message=f'Hello POST: \n\n{self.msg}')


# TODO: Refactor into TourPublic, TourPrivate, TourAdmin
# https://stackoverflow.com/questions/28822472/extending-the-behavior-of-an-inherited-function-in-python
# Use Inheritance and helper functions
# class TourPrivate():
#     def get():
#         tours = [_get_public(), _get_private()]
#         return tours

class ActivityAPI(MethodView):
    decorators = [user_status]

    def get(self, activity_id, user):
        if activity_id is None:
            activities = Activity.query.all()
            data = {'success': True,
                    'activities': [activity.to_dict() for activity in activities]}
        else:
            activity = Activity.query.get(activity_id)
            if activity is None:
                abort(404)
            data = {'success': True,
                    'activities': [activity.to_dict()]}

        return jsonify(data), 200

    def patch(self, activity_id, user):
        activity = Activity.query.get(activity_id)
        if activity is None:
            abort(404)
        if not user['auth']:
            abort(401)
        if not 'crud:activity' in user['permissions']:
            abort(403)

        body = request.get_json()
        activities = body.get('activities', [])
        if len(activities) != 1:
            abort(400)
        try:
            new_activity = activities[0]
            activity.name = new_activity['name']
            activity.description = new_activity['description']
            activity.update()
        except:
            abort(422)

        data = {'success': True,
                'activities': [activity.to_dict()]}

        return jsonify(data), 200

    def post(self, activity_id, user):
        pass

    def delete(self, activity_id, user):
        pass


class TourAPI(MethodView):
    decorators = [user_status]

    def get(self, tour_id, user):
        # GET All
        if tour_id is None:
            if user['auth']:
                if 'crud:tour:all' in user['permissions']:
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
                if user['auth']:
                    if 'crud:tour:all' in user['permissions']:
                        tours = [tour]
                    elif tour.user_id == user['id']:
                        tours = [tour]
                    else:
                        abort(403)
                else:
                    abort(401)
            else:
                tours = [tour]
        data = {'success': True,
                'tours': [tour.to_geojson() for tour in tours]}

        return jsonify(data), 200

    def patch(self, tour_id, user):
        authorized = False
        tour = Tour.query.get(tour_id)
        if tour is None:
            abort(404)

        if user['auth']:
            if 'crud:tour:all' in user['permissions']:
                authorized = True
            elif tour.user_id == user['id']:
                authorized = True
            else:
                abort(403)
        else:
            abort(401)

        if authorized:
            body = request.get_json()
            tours = body.get('tours', [])
            if len(tours) != 1:
                abort(400)
            try:
                new_tour = tours[0]
                tour.from_geojson(new_tour)
                tour.update()
            except:
                abort(422)

            data = {'success': True,
                    'tours': [tour.to_geojson()]}

            return jsonify(data), 200
        else:
            abort(500)

    def post(self, user, **kwargs):
        if not user['auth']:
            abort(401)

        authorized = 'crud:tour:own' in user['permissions']
        if not authorized:
            abort(401)

        body = request.get_json()
        tours = body.get('tours', [])
        if len(tours) != 1:
            abort(400)

        try:
            tour = Tour()
            tour.from_geojson(tours[0])
            tour.user_id = user['id']
            tour.insert()
        except:
            print("Unexpected error:", sys.exc_info())
            abort(500)

        data = {'success': True,
                'tours': [tour.to_geojson()]}
        return jsonify(data), 200

    def delete(self, tour_id, user):
        authorized = False
        tour = Tour.query.get(tour_id)
        if tour is None:
            abort(404)

        if user['auth']:
            if 'crud:tour:all' in user['permissions']:
                authorized = True
            elif tour.user_id == user['id']:
                authorized = True
            else:
                abort(403)
        else:
            abort(401)

        if authorized:
            try:
                tour.delete()
            except:
                abort(422)

            data = {'success': True,
                    'deleted': tour.id}
            return jsonify(data), 200
        else:
            abort(500)