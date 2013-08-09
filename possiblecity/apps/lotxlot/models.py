# lotxlot/models.py

import datetime

from django.contrib.gis.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from ..core.managers import CustomQuerySetGeoManager
from .managers import LotQuerySet

class Lot(models.Model):
    # spatial fields
    coord = models.PointField(srid=4326, blank=True, null=True)
    poly = models.MultiPolygonField(srid=4326, blank=True, null=True)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)

    is_visible = models.BooleanField(default=True)
    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
 
    #auto-generated fields
    slug = models.SlugField(max_length=255, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomQuerySetGeoManager(LotQuerySet)

    def __unicode__(self):
        if self.address:
            return u'%s' % (self.address)
        else:
            

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.address)
        super(LotBase, self).save(*args, **kwargs)
