# lotxlot/models.py

from django.contrib.gis.db import models
from django.db.models import permalink

from django.contrib.localflavor.us.models import USZipCodeField, USStateField

class LotBase(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    # spatial fields
    coord = models.PointField(blank=True, null=True)
    # should geom live here? or in concrete models?
    geom = models.MultiPolygonField(srid=4326, geography=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.address)

class USLotBase(LotBase):
    """
        This model defines a discreet piece of land within a municipality in the United States
    """
    state = models.USStateField
    zip_code = models.USZipCodeField
