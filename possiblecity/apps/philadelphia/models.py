# philadelphia/models.py
import urllib

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
            num_ideas=Count('ideas')).aggregate(Sum('num_ideas'))
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
    tencode = models.CharField(max_length=10, blank=True)
    brt_id = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    
    pwd_parcel = models.MultiPolygonField(srid=4326)

    lot = models.OneToOneField(Lot, null=True, blank=True, related_name='profile')
    neighborhood = models.ForeignKey(Neighborhood, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 

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

    def get_data_by_address(self, datasource, search_field, timeout=604800):
        source = datasource + "query"
        params = {"where":"%s=%s" % (search_field, urllib.quote_plus(self.address)),
                  "returnGeometry":"false",
                  "outFields":"*", "f":"json"}

        try:
            data =  fetch_json(source, params, timeout)
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        return features[0]["attributes"]
        except:
            return None


    def get_data_by_point(self, datasource, timeout=604800):
        pnt = self.get_center()
        lon = pnt.x
        lat = pnt.y
        source = datasource + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"*", "f":"json"}

        try:
            data =  fetch_json(source, params, timeout)

            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        return features[0]["attributes"]
        except:
            return None
    
    def get_data_by_envelope(self, datasource, timeout=604800):
        envelope = ', '.join(map(str, self.get_center().buffer(0.00008).extent))
        source = datasource + "query"
        params = {"geometry":"%s" % envelope, "geometryType":"esriGeometryEnvelope", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelContains",
                  "outFields":"*", "f":"json"}
        try:
            data =  fetch_json(source, params, timeout)
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        return features[0]["attributes"]
        except:
            return None

    def get_address_data(self):
        return self.get_data_by_point(settings.PHL_DATA["ADDRESSES"])

    def get_landuse_data(self):
        return self.get_data_by_point(settings.PHL_DATA["LAND_USE"], 2628000)

    def get_zoning_base(self):
        return self.get_data_by_point(settings.PHL_DATA["ZONING_BASE"], 2628000)

    def get_zoning_overlay(self):
        return self.get_data_by_point(settings.PHL_DATA["ZONING_OVERLAY"], 2628000)

    def get_zoning_flood(self):
        return self.get_data_by_point(settings.PHL_DATA["ZONING_FLOOD"], 2628000)

    def get_zoning_slope(self):
        return self.get_data_by_point(settings.PHL_DATA["ZONING_SLOPE"], 2628000)

    def get_service_council(self):
        return self.get_data_by_point(settings.PHL_DATA["SERVICE_COUNCIL"], 2628000)

    def get_service_planning(self):
        return self.get_data_by_point(settings.PHL_DATA["SERVICE_PLANNING"], 2628000)

    def get_service_census(self):
        return self.get_data_by_point(settings.PHL_DATA["SERVICE_CENSUS"], 2628000)

    def get_service_blockgroup(self):
        return self.get_data_by_point(settings.PHL_DATA["SERVICE_BLOCKGROUP"], 2628000)

    def get_service_ward(self):
        return self.get_data_by_point(settings.PHL_DATA["SERVICE_WARD"], 2628000)

    def get_licenses(self):
        return self.get_data_by_envelope(settings.PHL_DATA["VACANCY_LICENSES"])

    def get_violations(self):
        data = self.get_data_by_address(
                   settings.PHL_DATA["VACANCY_VIOLATIONS"], 'VIOLATION_ADDRESS')
        if data:
            return data
        else:
            return self.get_data_by_envelope(settings.PHL_DATA["VACANCY_VIOLATIONS"])

    def get_opa_data(self):
        source = settings.PHL_DATA["ADDRESS_API"] + urllib.quote_plus(self.address)
        params = ''

        try:
            data = fetch_json(source, params, 604800)
            if "property" in data:
                return data["property"]
        except:
            return None

    def get_papl_listing(self):
        return self.get_data_by_envelope(settings.PHL_DATA["PAPL_LISTINGS"])

    @property
    def papl_listing(self):
        return self.get_papl_listing()    

    @property
    def account_mailing_address(self):
        return self.get_opa_data()['account_information']['mailing_address']

    @property
    def account_details(self):
        return self.get_opa_data()['account_details']

    @property
    def account_valuation(self):
        return self.get_opa_data()['valuation_details']['2014']

    @property
    def address_data(self):
        return self.get_address_data()

    @property
    def violation_set(self):
        pass

    @property
    def is_for_sale(self):
        if self.get_papl_listing():
            return True
        else:
            return False

    @property
    def has_violation(self):
        if self.get_violations():
            return True
        else:
            return False

    @property
    def has_license(self):
        if self.get_licenses():
            return True
        else:
            return False

    @property
    def is_non_compliant(self):
        if self.has_violation:
            if self.latest_violation["VIOLATION_STATUS"] == "Not Complied":
                return True
            else:
                return False
        else:
            return False

    @property
    def is_land_use_vacant(self):
        if self.land_use == "Vacant Parcels":
            return True
        else:
            return False

    @property
    def is_bldg_desc_vacant(self):
        if self.building_description and "Vac" in self.building_description:
            return True
        else:
            return False         

    @property
    def owner(self):
        owner = self.get_address_data()["OWNER1"].title()
        if self.get_address_data()["OWNER2"]:
            owner = owner + " / " + self.get_address_data()["OWNER2"].title()

        return owner

    @property
    def building_description(self):
        if self.get_address_data() and self.get_address_data()["BLDG_DESC"]:
            return "%s (%s)" % (self.get_address_data()["BLDG_DESC"].title(), self.get_address_data()["BLDG_CODE"])
        else:
            return None

    @property
    def impervious_area(self):
        try:
            return "%s sq ft" % (self.get_address_data()["IMPERV_AREA"])
        except KeyError:
            pass

    @property
    def land_use(self):
        try: 
            return self.get_landuse_data()["C_DIG3DESC"]
        except KeyError:
            pass

        try:
            return self.get_landuse_data()["C_DIG2DESC"]
        except KeyError:
            pass
            
        try:
            return self.get_landuse_data()["C_DIG1DESC"]
        except KeyError:
            return None

    @property
    def zoning_base(self):
        return self.get_zoning_base()["LONG_CODE"]

    @property
    def zoning_overlay(self):
        return self.get_zoning_overlay()

    @property
    def zoning_flood(self):
        return self.get_zoning_flood()

    @property
    def zoning_slope(self):
        return self.get_zoning_slope()

    @property
    def council_district(self):
        return self.get_service_council()

    @property
    def planning_district(self):
        return self.get_service_planning()

    @property
    def census(self):
        return self.get_service_census()

    @property
    def blockgroup(self):
        return self.get_service_blockgroup()

    @property
    def ward(self):
        return self.get_service_ward()

    @property
    def latest_violation(self):
        return self.get_violations()

    @property
    def latest_license(self):
        return self.get_licenses()

    @property
    def papl_price(self):
        if self.get_papl_listing():
            return self.get_papl_listing()["PRICE_STR"]

    @property
    def papl_asset_id(self):
        if self.get_papl_listing():
            return self.get_papl_listing()["ASSET_ID"]


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

