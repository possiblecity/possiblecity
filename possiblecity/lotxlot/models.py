# lotxlot/models.py

import datetime

from django.contrib.gis.db import models
from django.db.models import permalink

from django.contrib.localflavor.us.models import USStateField
from django.template.defaultfilters import slugify

from possiblecity.core.managers import CustomQuerySetGeoManager
from .managers import LotQuerySet

class LotBase(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)
    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
 
    #auto-generated fields
    slug = models.SlugField(max_length=255, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # spatial fields
    coord = models.PointField(srid=4326, blank=True, null=True)
    geom = models.MultiPolygonField(srid=4326)

    objects = CustomQuerySetGeoManager(LotQuerySet)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.address)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.address)
        super(LotBase, self).save(*args, **kwargs)

class USLotBase(LotBase):
    """
        This model defines a discreet piece of land within a municipality in the United States
    """
    state = USStateField()
    zip = models.CharField(max_length=10)

    class Meta:
        abstract = True
