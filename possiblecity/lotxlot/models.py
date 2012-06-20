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
    is_visible = models.BooleanField(default=True)

    # spatial fields
    coord = models.PointField(blank=True, null=True)
    # should geom live here? or in concrete models? 
    # geom =  

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % (self.address)

    #@models.permalink
    #def get_absolute_url(self):
       #return ('', [)])

    def save(self, *args, **kwargs):
        """
           Make sure the model has coordinates and an address.
           If there are no coordinates, first try to get them from
           the geom field. If there is no geom field, get the coordinates
           by reverse geocoding the address. If there are coordinates and no
           address, geocode the coordinates.

           If the address, geometry, or coordinates change, make sure they are 
           all in sync. 
        """
        pass
