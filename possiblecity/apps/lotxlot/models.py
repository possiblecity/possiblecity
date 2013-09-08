# lotxlot/models.py

import datetime

from django.contrib.gis.db import models
from django.contrib.gis.measure import Area
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.template.defaultfilters import slugify

#from ..core.managers import CustomQuerySetGeoManager
from .managers import LotQuerySet
from .fields import AutoOneToOneField

class Lot(models.Model):
    # spatial fields
    coord = models.PointField(srid=4326, blank=True)
    bounds = models.MultiPolygonField(srid=4326, blank=True)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True)

    is_visible = models.BooleanField(default=True)
    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
 
    #auto-generated fields
    slug = models.SlugField(max_length=255, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #objects = CustomQuerySetGeoManager(LotQuerySet)
    objects = models.GeoManager()

    class Meta:
        pass
        #unique_together = ('address', 'city', 'state')

    def get_sqft(self): 
        """ 
        Returns the area in sq ft. 
        """ 
        # Convert our geographic polygons (in WGS84)
        # into a local projection for New York (here EPSG:32118) 
        try:
            return self.bounds.transform(102729, clone=True).area
        except Exception:
            return None

    def get_acres(self): 
        """ 
        Returns the area in sq ft. 
        """ 
        # Convert our geographic polygons (in WGS84)
        # into a local projection for New York (here EPSG:32118) 
        try:
            return self.bounds.transform(102729, clone=True).area * 0.00002295684
        except Exception:
            return None
        

    def __unicode__(self):
        if self.address:
            return u'%s' % (self.address)
        elif self.coord:
            return u'(%s,%s)' % (self.coord.x, self.coord.y)
        else:
            return u'No Address %s' % (self.pk)

    @permalink
    def get_absolute_url(self):
        kwargs = { 'id': self.id }
        return reverse("lotxlot_lot_detail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.address:
                slug = '%s %s, %s' % (self.address, self.city, self.state)
            elif self.coord:
                slug = '(%s,%s) %s, %s' % (self.coord.x, self.coord.y, self.city, self.state)
            else:
                slug = 'No Address %s %s, %s' % (self.pk, self.city, self.state)
            self.slug = slugify(slug)
        super(Lot, self).save(*args, **kwargs)



class BaseBoundary(models.Model):
    """
    A shape that defines an area
    """

    lot = models.OneToOneField(Lot)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseDataSource(models.Model):
    """
    An abstract data source attached to a lot which may need
    to be periodically updated
    """

    lot = models.OneToOneField(Lot)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

