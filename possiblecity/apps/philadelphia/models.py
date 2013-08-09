# philadelphia/models.py

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save


class Neighborhood(models.Model):
    """
    Information about a Philadelphia neighborhood
    """
    pass

class LotProfile(models.Model):
    """
    City specific information about an individual unit of land in Philadelphia
    """
    neighborhood
    basereg
    opa_code
    address
    geom = model.MultiPolygonField(srid=4269)