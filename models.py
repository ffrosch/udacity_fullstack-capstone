from datetime import datetime

from sqlalchemy import func, ForeignKey, Column, Date, Integer, String, Time
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .app import db


class Tour(db.Model):
    """A tour/trip, including its geospatial data."""

    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date, nullable=False)
    starttime = Column(Time)
    endtime = Column(Time)
    accesslevel_id = Column(Integer, ForeignKey('accesslevels.id'))
    startpoint = Column(Geometry(geometry_type="POINT"), nullable=False)
    endpoint = Column(Geometry(geometry_type="POINT"))
    path = Column(Geometry(geometry_type="LINESTRING"))


class Activity(db.Model):
    """An outdoor activity."""

    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tours = relationship("Tour")


class Accesslevel(db.Model):
    """Access levels define who has access to an entry.

    Levels:
    - Public
    - Friend
    - Private"""

    __tablename__ = 'accesslevels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tours = relationship("Tour")


class Region(db.Model):
    """List of geographic regions within a country."""

    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(Integer, ForeignKey('countries.id'))
    geom = Column(Geometry(geometry_type="MULTIPOLYGON"))


class Country(db.Model):
    """List of countries."""

    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    regions = relationship("Region")
    geom = Column(Geometry(geometry_type="MULTIPOLYGON"))
