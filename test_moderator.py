import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Accesslevel, Tour, Activity
from config import Config


database_name = 'capstone_test'
database_path = f'postgresql://localhost:5432/{database_name}'

JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxzRmtSb3RnTnJnWUF3R25vUjI1MCJ9.eyJpc3MiOiJodHRwczovL3N0dXJtcHVscy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyN2Y1Nzg3MjY2NjUwMDZhMmFhM2UwIiwiYXVkIjoidWRhY2l0eS1jYXBzdG9uZS1iYWNrZW5kIiwiaWF0IjoxNjEzMzQ0NjQyLCJleHAiOjE2MTM0MzEwNDIsImF6cCI6IlluaDFDRVJBVVVJWTRYcVUzMmNCczR4VmlPOUVYaFFHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcnVkOmFjdGl2aXR5IiwiY3J1ZDp0b3VyOm93biJdfQ.JncB0bo3pzXqvDGQcghwZjSDjaUFyyzaPek5_0WjeCQub6uT5xFisg_ZgWKpn6z9stU4nqjdHe-0ZXxhwGFnnJT9B-Xvlulom50PZMX1wAY5T5lI4E7Oc1fe7TH3H1QTUEukzsg_NPcO1CdDUMF8EFEw2aVJW1z2W5J_ci9XdPnanu-6wUwlFWvpgDfkqa4FxsFTD-tt9GK6EKJHtRs1JUrqHczr3oYVPWYi3QEx4Oa9iQesrEy6l7ldB4AdI0QEQcjM3hSD3WM38ZN3RHAUQYgshEo1WTfRpO9Kqal5SmVCRPieS-Nla4IWircREGKuX7qLOemZ6vMqGRH5cU-vtA'  # nopep8
HEADERS = {'Authorization': f'Bearer {JWT}'}


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = database_path


class TestUser(unittest.TestCase):
    '''This class represents the Tour test case.'''

    def setUp(self):
        '''Define test variables and initialize app.'''

        self.app = create_app(TestConfig)
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        a1 = Accesslevel(name='Public')
        a2 = Accesslevel(name='Private')
        db.session.add_all([a1, a2])
        db.session.commit()

        act1 = Activity(name='Mountainbiking',
                        description='Riding your bike on trails')
        act2 = Activity(name='Mountaineering',
                        description='Ascending a mountain')
        db.session.add_all([act1, act2])
        db.session.commit()

        t1 = Tour(user_id='auth0|6027f561c6ce2e00695ffda9', activity_id=1,
                  name='Admin Entry', date='2021-02-13', accesslevel_id=1,
                  location='SRID=4326;POINT(7.1 46.1)')
        t2 = Tour(user_id='auth0|6027f578726665006a2aa3e0', activity_id=2,
                  name='Moderator Entry', date='2020-06-06', accesslevel_id=2,
                  location='SRID=4326;POINT(8.2 47.2)')
        t3 = Tour(user_id='auth0|6027f5187e20570068ba16bd', activity_id=1,
                  name='User Entry', date='2019-12-01', accesslevel_id=1,
                  location='SRID=4326;POINT(9.3 48.3)')
        db.session.add_all([t1, t2, t3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

################
#   Tour API   #
################

# GET #
    def test_get_tours(self):
        res = self.client().get('/api/tours/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['tours']), 2)

    def test_get_tour_private_own(self):
        res = self.client().get('/api/tours/2', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

####################
#   Activity API   #
####################

# PATCH #
    def test_patch_activity(self):
        '''RBAC based'''
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        res = self.client().patch('/api/activities/1', json=act,
                                  headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_patch_activity_400(self):
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        act['activities'] = [act['activities'][0], act['activities'][0]]
        res = self.client().patch('/api/activities/1', json=act,
                                  headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_patch_activity_404(self):
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        res = self.client().patch('/api/activities/99',
                                  json=act, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_patch_activity_422(self):
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        del act['activities'][0]['name']
        res = self.client().patch('/api/activities/1',
                                  json=act, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

# POST #
    def test_post_activity(self):
        '''RBAC based'''
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        res = self.client().post('/api/activities/', json=act, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_post_activity_422(self):
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        del act['activities'][0]['name']
        res = self.client().post('/api/activities/', json=act, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

# DELETE #
    def test_delete_activity_404(self):
        res = self.client().delete('/api/activities/1', headers=HEADERS)
        act = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_delete_activity(self):
        '''RBAC based'''
        res = self.client().delete('/api/activities/999', headers=HEADERS)
        act = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
