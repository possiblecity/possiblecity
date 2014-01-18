# lotxlot/models.py

import datetime
import os

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.gis.db import models
from django.contrib.gis.measure import Area
from django.contrib.gis.db.models.query import GeoQuerySet
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.template.defaultfilters import slugify

from apps.core.managers import PassThroughGeoManager

from apps.comments.models import Comment

class LotQuerySet(GeoQuerySet):
    def visible(self):
        return self.filter(is_visible=True)

    def vacant(self):
        return self.filter(is_vacant=True)

    def public(self):
        return self.filter(is_public=True)

    def private(self):
        return self.filter(is_public=False)


class Lot(models.Model):
    # spatial fields
    coord = models.PointField(srid=4326, blank=True)
    bounds = models.MultiPolygonField(srid=4326, blank=True)
    area = models.FloatField(db_index=True, blank=True)

    address = models.CharField(db_index=True, max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True)

    # meta fields
    is_visible = models.BooleanField(db_index=True, default=True)
    is_vacant = models.BooleanField(db_index=True, default=False)
    is_public = models.BooleanField(db_index=True, default=False)
 
    #auto-generated fields
    slug = models.SlugField(max_length=255, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    comments = generic.GenericRelation(Comment)

    objects = PassThroughGeoManager.for_queryset_class(LotQuerySet)()

    class Meta:
        pass

    @property 
    def activity_count(self):
        activity = self.comments.count() + self.ideas.count()
        return activity

    @property
    def has_project(self):
        if self.ideas:
            return True
        else:
            return False

    @property
    def has_comment(self):
        if self.comments:
            return True
        else:
            return False

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

    def get_absolute_url(self):
        return reverse('lotxlot_lot_detail', args=[str(self.id)])

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


