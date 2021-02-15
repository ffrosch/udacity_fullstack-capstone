from app import create_app, db
from app.models import Accesslevel, Tour, Activity
from config import Config


app = create_app(Config)
app_context = app.app_context()
app_context.push()
db.drop_all()
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
