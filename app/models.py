import json

from datetime import datetime

from sqlalchemy import func, ForeignKey, Column, Date, Integer, String, Time
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

from app import db


class Tour(db.Model):
    """A tour/trip, including its geospatial data."""

    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    starttime = Column(Time)
    endtime = Column(Time)
    accesslevel_id = Column(Integer, ForeignKey('accesslevels.id'), nullable=False)
    location = Column(Geometry(geometry_type="POINT",
                               srid=4326), nullable=False)

    def from_geojson(self, data):
        coords = data['coordinates']
        props = data['properties']

        self.activity_id = props['activity']['id']
        self.name = props['name']
        self.description = props['description']
        self.date = props['date']
        self.starttime = props['starttime']
        self.endtime = props['endtime']
        self.accesslevel_id = props['accesslevel']['id']
        self.location = f'SRID=4326;POINT({coords[0]} {coords[1]})'

    def __repr__(self):
        return f'<{self.name}, {self.date}, {self.geo_text}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def geo_srid(self):
        srid = db.session.scalar(self.location.ST_SRID())
        return srid

    @property
    def geo_text(self):
        try:
            txt = db.session.scalar(self.location.ST_AsText())
        except:
            txt = None
        return txt

    @property
    def XY(self):
        X = db.session.scalar(self.location.ST_X())
        Y = db.session.scalar(self.location.ST_Y())
        return X, Y

    def as_geojson(self):
        geo = db.session.scalar(self.location.ST_AsGeoJSON())
        data = json.loads(geo)
        data['properties'] = {
            'id': self.id,
            'activity': {
                'id': self.activity.id,
                'name': self.activity.name,
                'description': self.activity.id
            },
            'name': self.name,
            'description': self.description,
            'date': self.date.isoformat(),
            'starttime': self.starttime,
            'endtime': self.endtime,
            'accesslevel': {
                'id': self.accesslevel.id,
                'name': self.accesslevel.name
            },
        }
        return data

    def as_shape(self):
        # TODO: For future use
        return to_shape(self.location)


class Activity(db.Model):
    """An outdoor activity."""

    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tours = relationship("Tour", backref='activity', lazy='dynamic',
                         cascade="save-update")


class Accesslevel(db.Model):
    """Access levels define who has access to an entry.

    Levels:
    - Public
    (- Friend) -> Future Release
    - Private"""

    __tablename__ = 'accesslevels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tours = relationship("Tour", backref='accesslevel', lazy='dynamic',
                         cascade="save-update")
