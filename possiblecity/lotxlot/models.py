# lotxlot/models.py

from django.contrib.gis.db import models
from django.db.models import permalink

class DataSource(models.Model):
    pass

class LotBase(models.Model):
    """
        This model defines a discreet piece of land within a municipality
    """

    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    # spatial fields
    coordinates = models.PointField(blank=True, null=True)

    class Meta:
        abstract = True