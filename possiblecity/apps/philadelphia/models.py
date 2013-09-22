# philadelphia/models.py

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.db.models import Count, Sum

from apps.lotxlot.models import Lot
from apps.lotxlot.utils import fetch_json

class Neighborhood(models.Model):
    """
    Information about a Philadelphia neighborhood
    """
    objects = models.GeoManager()

    name = models.CharField(max_length=255)
    map_name = models.CharField(max_length=255)
    list_name = models.CharField(max_length=255)
    bounds = models.MultiPolygonField(srid=4326)

    @property
    def vacant_lot_count(self):
        return Lot.objects.filter(is_vacant=True).filter(coord__within=self.bounds).count()

    @property
    def idea_count(self):
        qs = Lot.objects.filter(
            is_vacant=True).filter(
            coord__within=self.bounds).annotate(
            num_ideas=Count('idea')).aggregate(Sum('num_ideas'))
        return qs["num_ideas__sum"]


    class Meta:
        ordering = ['name']    

    def __unicode__(self):
        return u'%s' % self.map_name

class LotProfile(models.Model):
    """
    City specific information about an individual unit of land in Philadelphia.
    """
    objects = models.GeoManager()

    basereg = models.CharField(max_length=10, blank=True) 
    opa_code = models.CharField( max_length=10, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    pwd_parcel = models.MultiPolygonField(srid=4326)

    lot = models.OneToOneField(Lot, null=True, blank=True, related_name='profile')
    neighborhood = models.ForeignKey(Neighborhood, null=True, blank=True)

    def get_center(self):
        try:
            center = self.pwd_parcel.point_on_surface
        except:
            center = self.pwd_parcel.centroid
        return center

    def get_neighborhood(self):
         pnt = self.get_center()
         qs = Neighborhood.objects.filter(bounds__contains=pnt)
         return qs[0]

    def get_address_data(self):
        pnt = self.get_center()
        lon = pnt.x
        lat = pnt.y
        source = settings.PHL_DATA["ADDRESSES"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"OWNER1, OWNER2, BLDG_CODE, BLDG_DESC, IMPERV_AREA ", "f":"json"}

        data =  fetch_json(source, params, 604800)

        if "features" in data:
            features = data["features"]
            if features:
                if features[0]:
                    return features[0]["attributes"]

    @property
    def owner(self):
        owner = self.get_address_data()["OWNER1"].title()
        if self.get_address_data()["OWNER2"]:
            owner = owner + " / " + self.get_address_data()["OWNER2"].title()

        return owner

    @property
    def building_description(self):
        return "%s (%s)" % (self.get_address_data()["BLDG_DESC"].title(), self.get_address_data()["BLDG_CODE"])

    @property
    def impervious_area(self):
        return "%s sq ft" % (self.get_address_data()["IMPERV_AREA"])


    def __unicode__(self):
        return u'%s' % self.lot

    def save(self, *args, **kwargs):
        if not self.neighborhood:
            self.neighborhood = self.get_neighborhood()
        super(LotProfile, self).save(*args, **kwargs)

def lot_profile_post_save(sender, **kwargs):
    """
        When a LotProfile instance is created, create a related Lot instance.
        Then use its address data and geometry data to update the related
        Lot address and bounds fields, respectively.
    """
    lot_profile, created = kwargs["instance"], kwargs["created"]
    # if this is a new instance of parcel, 
    # create and populate the related Lot
    if created:
        lot = Lot(address=lot_profile.address.title(),
            bounds=lot_profile.pwd_parcel, 
            coord=lot_profile.get_center(),
            city='Philadelphia', state='PA', country='US',)
        lot.save()
        lot_profile.lot = lot
        lot_profile.save()

post_save.connect(lot_profile_post_save, sender=LotProfile)

