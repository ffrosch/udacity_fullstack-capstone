SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid()AND datname = 'udacity-capstone'; \q


insert into accesslevels (name) values ('Public');
insert into accesslevels (name) values ('Private');
insert into activities (name, description) values ('Mountainbiking', 'Riding your Bike on Trails');
insert into activities (name, description) values ('Mountaineering', 'Ascending a mountain where at least an ice axe and crampons are required');
insert into tours (user_id, activity_id, name, date, accesslevel_id, location) values (1, 1, 'Hinterzarten', '2019-01-01', 1, ST_GeomFromText('POINT(8.0 47.9)', 4326));
insert into tours (user_id, activity_id, name, date, accesslevel_id, location) values (1, 1, 'Gardasee', '2016-06-07', 2, ST_GeomFromText('POINT(10.7 45.6)', 4326));
insert into tours (user_id, activity_id, name, date, accesslevel_id, location) values (2, 2, 'Matterhorn', '2013-08-15', 1, ST_GeomFromText('POINT(7.6584831 45.9764535)', 4326));