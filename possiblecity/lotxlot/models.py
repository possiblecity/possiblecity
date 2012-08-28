# lotxlot/models.py

from django.contrib.gis.db import models
from django.db.models import permalink

from django.contrib.localflavor.us.models import USStateField
from django.templates.defaultfilters import slugify

class LotBase(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    is_vacant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    slug = models.CharField(max_length=255, editable=False)

    # spatial fields
    coord = models.PointField(blank=True, null=True)
    # should geom live here? or in concrete models?
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.address)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.address)
        super(test, self).save(*args, **kwargs)

class USLotBase(LotBase):
    """
        This model defines a discreet piece of land within a municipality in the United States
    """
    state = USStateField()
    zip = models.CharField(max_length=10)

    class Meta:
        abstract = True
