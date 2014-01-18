# core/managers.py
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet

from model_utils.managers import PassThroughManagerMixin

class PassThroughGeoManager(PassThroughManagerMixin, models.GeoManager):
    pass
    