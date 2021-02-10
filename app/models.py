from datetime import datetime

from sqlalchemy import func, ForeignKey, Column, Date, Integer, String, Time
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from app import db


class Tour(db.Model):
    """A tour/trip, including its geospatial data."""

    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    starttime = Column(Time)
    endtime = Column(Time)
    accesslevel_id = Column(Integer, ForeignKey('accesslevels.id'))
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)


class Activity(db.Model):
    """An outdoor activity."""

    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tours = relationship("Tour", cascade="all, delete-orphan")


class Accesslevel(db.Model):
    """Access levels define who has access to an entry.

    Levels:
    - Public
    (- Friend) -> Future Release
    - Private"""

    __tablename__ = 'accesslevels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tours = relationship("Tour", cascade="all, delete-orphan")
