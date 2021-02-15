import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Accesslevel, Tour, Activity
from config import Config


database_name = 'capstone_test'
database_path = f'postgresql://localhost:5432/{database_name}'

JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxzRmtSb3RnTnJnWUF3R25vUjI1MCJ9.eyJpc3MiOiJodHRwczovL3N0dXJtcHVscy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyN2Y1MTg3ZTIwNTcwMDY4YmExNmJkIiwiYXVkIjoidWRhY2l0eS1jYXBzdG9uZS1iYWNrZW5kIiwiaWF0IjoxNjEzMzQzMjE3LCJleHAiOjE2MTM0Mjk2MTcsImF6cCI6IlluaDFDRVJBVVVJWTRYcVUzMmNCczR4VmlPOUVYaFFHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcnVkOnRvdXI6b3duIl19.bExzyhoy9xOkBaiFc4W9IhWPlCIvi_Bg5lZeF1hlExqFP12JtfXNlZNXUHS67y5yE-yP5vPBDp52yG7ODcKBa9xZKUZY9fAbWHZwt_7tia9UkT6a8qO5JJbUmlrnp6sdXaXKsD6qO_zZ1QAicDd4hLVq61qVC8u0BZDmadlhtR01NBOX717jD2Brthx4A8snS1FEToXgfndHyylxl5oPjOBVhV99cTVOBsikJGMNNZ7rj0002W_T78wTMQU2IKuzmtPv8HwzelxaC2wqtvQzXFdMiyYxiwK6sNBbwhWsEFUWm3Vq8mMF7Zp1OhTTuRg2sFqvxNOiun8RruydmuDTJA'
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
### Tour API ###
################

### GET ###
    def test_get_tours(self):
        res = self.client().get('/api/tours/', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['tours']), 2)

    def test_get_tour_public(self):
        res = self.client().get('/api/tours/1', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_tour_private_other_403(self):
        '''RBAC based'''
        res = self.client().get('/api/tours/2', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])

### PATCH ###
    def test_patch_tour_other_403(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/1', headers=HEADERS)
        t = json.loads(req.data)

        res = self.client().patch('/api/tours/1', json=t, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_patch_tour_own(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/3', headers=HEADERS)
        t = json.loads(req.data)

        res = self.client().patch('/api/tours/3', json=t, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

### DELETE ###
    def test_delete_tour_other_403(self):
        '''RBAC based'''
        res = self.client().delete('/api/tours/1', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_delete_tour_own(self):
        '''RBAC based'''
        res = self.client().delete('/api/tours/3', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

### POST ###
    def test_post_tour(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/1', headers=HEADERS)
        t = json.loads(req.data)
        res = self.client().post('/api/tours/', json=t, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_post_tour_400(self):
        req = self.client().get('/api/tours/1', headers=HEADERS)
        t = json.loads(req.data)
        t['tours'] = [t['tours'][0], t['tours'][0]]
        res = self.client().post('/api/tours/', json=t, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)



####################
### Activity API ###
####################

### Get ###
    def test_get_activities(self):
        res = self.client().get('/api/activities/', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

### Post ###
    def test_post_activity_403(self):
        '''RBAC based'''
        req = self.client().get('/api/activities/1', headers=HEADERS)
        act = json.loads(req.data)
        res = self.client().post('/api/activities/', json=act, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

if __name__ == '__main__':
    unittest.main(verbosity=2)
