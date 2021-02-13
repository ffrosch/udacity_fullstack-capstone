psql -d udacity-capstone -c  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid()AND datname = 'udacity-capstone';"

dropdb udacity-capstone
createdb udacity-capstone
psql -d udacity-capstone -c 'create extension postgis;'
psql -d udacity-capstone -c "insert into accesslevels (name) values ('Public'), ('Private');"
psql -d udacity-capstone -c "insert into activities (name, description) values ('Mountainbiking', 'Riding your Bike on Trails'), ('Mountaineering', 'Ascending a mountain where at least an ice axe and crampons are required');"


Tour(user_id='auth0|6027f561c6ce2e00695ffda9', activity_id=1, name='Admin Entry', date='2021-02-13', accesslevel_id=1, location='SRID=4326;POINT(7.1 46.1)').insert()
Tour(user_id='auth0|6027f578726665006a2aa3e0', activity_id=2, name='Moderator Entry', date='2020-06-06', accesslevel_id=2, location='SRID=4326;POINT(8.2 47.2)').insert()
Tour(user_id='auth0|6027f5187e20570068ba16bd', activity_id=1, name='User Entry', date='2019-12-01', accesslevel_id=1, location='SRID=4326;POINT(9.3 48.3)').insert()
