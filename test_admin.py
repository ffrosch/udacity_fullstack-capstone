import json
import unittest
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models import Accesslevel, Tour, Activity
from config import Config


database_name = 'capstone_test'
database_path = f'postgresql://localhost:5432/{database_name}'

JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxzRmtSb3RnTnJnWUF3R25vUjI1MCJ9.eyJpc3MiOiJodHRwczovL3N0dXJtcHVscy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyN2Y1NjFjNmNlMmUwMDY5NWZmZGE5IiwiYXVkIjoidWRhY2l0eS1jYXBzdG9uZS1iYWNrZW5kIiwiaWF0IjoxNjEzMzQ3MTk5LCJleHAiOjE2MTM0MzM1OTksImF6cCI6IlluaDFDRVJBVVVJWTRYcVUzMmNCczR4VmlPOUVYaFFHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcnVkOmFjdGl2aXR5IiwiY3J1ZDp0b3VyOmFsbCIsImNydWQ6dG91cjpvd24iXX0.HlywLJiEGp4X_wBx1lCv88o9nVky7gd8l-LDs85eEXxK1onuxj_nfq0hZk-jmnRsP_S-UoDq_T8kmzBSPasJo2Sk6TzS_5CnRc03mSEjL9rehSB1SfGZA2V9aJkMrevnOwVc_PyS9L0McaPER71ILZAVzylw69J7hs0dD9kZAGJP7cIo2uTzDnyBPQFcH5StDk5DIuHTM8OmxEFpLlSC5UENk_5gQvYqOLpEulQVNKb5v5tHg4cxviecHFzdTnDhW_ozUFSFS5k2PrTz2dXlbK8HEsWE_n4hnt_nn5woGMsh9owOxBzBYaWR2Ng6ygdQLnqhR-OQdGZzsNpCY7zLtg'
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
        '''RBAC based'''
        res = self.client().get('/api/tours/', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['tours']), 3)

    def test_get_tour_private_other(self):
        '''RBAC based'''
        res = self.client().get('/api/tours/2', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

### PATCH ###
    def test_patch_tour_other(self):
        '''RBAC based'''
        req = self.client().get('/api/tours/3', headers=HEADERS)
        t = json.loads(req.data)

        res = self.client().patch('/api/tours/3', json=t, headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

### DELETE ###
    def test_delete_tour_other(self):
        '''RBAC based'''
        res = self.client().delete('/api/tours/3', headers=HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
