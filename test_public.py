import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Accesslevel, Tour, Activity
from config import Config


database_name = 'capstone_test'
database_path = f'postgresql://localhost:5432/{database_name}'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = database_path


class TestPublic(unittest.TestCase):
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

    def test_get_tour_public(self):
        res = self.client().get('/api/tours/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_tour_public_404(self):
        res = self.client().get('/api/tours/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_tour_private_401(self):
        '''RBAC based'''
        res = self.client().get('/api/tours/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_tour_405(self):
        res = self.client().put('/api/tours/')

        self.assertEqual(res.status_code, 405)

# PATCH #
    def test_patch_tour_401(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/1')
        t = json.loads(req.data)
        res = self.client().patch('/api/tours/1', json=t)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

# DELETE #
    def test_delete_tour_401(self):
        '''RBAC based'''
        res = self.client().delete('/api/tours/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

# POST #
    def test_post_tour_401(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/1')
        t = json.loads(req.data)
        res = self.client().post('/api/tours/', json=t)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

####################
#   Activity API   #
####################

# GET #
    def test_get_activities(self):
        res = self.client().get('/api/activities/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_activity(self):
        res = self.client().get('/api/activities/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_get_activity_404(self):
        res = self.client().get('/api/activities/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
