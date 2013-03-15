# philadelphia/models.py

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save

from possiblecity.lotxlot.utils import fetch_json, has_feature
from possiblecity.lotxlot.models import USLotBase
from possiblecity.float.models import Project

class Lot(USLotBase):
    """
    A unit of land in Philadelphia, PA
    """
    # spatial queryset manager defined in parent class
     
    parcel = models.OneToOneField("Parcel", blank=True, null=True)

    is_available = models.BooleanField(default=False)
    has_vacancy_violation = models.BooleanField(default=False)
    has_vacancy_license = models.BooleanField(default=False)
    has_vacant_building = models.BooleanField(default=False)    
    
    # ids for external data sources
    address_id = models.IntegerField(blank=True, null=True)
    landuse_id = models.IntegerField(blank=True, null=True)
    papl_parcel_id = models.IntegerField(blank=True, null=True)
    papl_listing_id = models.IntegerField(blank=True, null=True)
    papl_asset_id = models.IntegerField(blank=True, null=True)
    vacancy_violation_id = models.IntegerField(blank=True, null=True)
    vacancy_license_id = models.IntegerField(blank=True, null=True)
    vacancy_appeal_id = models.IntegerField(blank=True, null=True)
    demolition_id = models.IntegerField(blank=True, null=True)
    demolition_permit_id = models.IntegerField(blank=True, null=True)


    def _get_coordinates(self):
        # get coordinates from geom field
        return self.geom.centroid

    def _get_zip(self):
        # TODO: determine zip code from address, city and state
        pass

    def _get_vacancy_violation_id(self):
        if self.vacancy_violation_id:
            return self.vacancy_violation_id
        else:
            source = settings.PHL_DATA["VACANCY_VIOLATIONS"] + "query"
            params = {"where":"VIOLATION_ADDRESS='%s'" % (self.address), "returnIdsOnly":"true", "f":"json"}
       
            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]

    def _get_vacancy_appeal_id(self):
        if self.vacancy_appeal_id:
            return self.vacancy_appeal_id
        else:
            source = settings.PHL_DATA["VACANCY_APPEALS"] + "query"
            params = {"where":"APPEAL_ADDRESS='%s'" % (self.address), "returnIdsOnly":"true", "f":"json"}

            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]        
   
    def _get_vacancy_license_id(self):
        if self.vacancy_license_id:
            return self.vacancy_license_id
        else:
            source = settings.PHL_DATA["VACANCY_LICENSES"] + "query"
            params = {"where":"LICENSE_ADDRESS='%s'" % (self.address), "returnIdsOnly":"true", "f":"json"}
        
            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                     return dict["objectIds"][0]
  
    def _get_demolition_id(self):
        if self.demolition_id:
            return self.demolition_id
        else:
             source = settings.PHL_DATA["VACANCY_DEMOLITIONS"] + "query"
             params = {"where":"LICENSE_ADDRESS='%s'" % (self.address), "returnIdsOnly":"true", "f":"json"}

             dict =  fetch_json(source, params)
             if dict and "objectIds" in dict:
                 if dict["objectIds"]:
                      return dict["objectIds"][0]

    def _get_demolition_permit_id(self):
        if self.demolition_permit_id:
            return self.demolition_permit_id
        else:
            source = settings.PHL_DATA["VACANCY_DEMOLITIONS"] + "query"
            params = {"where":"PERMIT_ADDRESS='%s'" % (self.address), "returnIdsOnly":"true", "f":"json"}

            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]


    def _get_papl_listing_id(self):
        if self.papl_listing_id:
            return self.papl_listing_id
        else:
            address = self.address.title()
            source = settings.PHL_DATA["PAPL_LISTINGS"] + "query"
            params = {"where":"REF_ADDRES='%s'" % (address), "returnIdsOnly":"true", "f":"json"}

            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]

    def _get_papl_asset_id(self):
        if self.papl_asset_id:
            return self.papl_asset_id
        else:
            address = self.address.title()
            source = settings.PHL_DATA["PAPL_ASSETS"] + "query"
            params = {"where":"REF_ADDRES='%s'" % (address), "returnIdsOnly":"true", "f":"json"}

            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]

    def _get_landuse_id(self):
        if self.landuse_id:
            return self.landuse_id
        else:
            lon = self.coord.x
            lat = self.coord.y
            source = settings.PHL_DATA["LAND_USE"] + "query"
            params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                      "inSR":"4326", "spatialRel":"esriSpatialRelWithin", "returnIdsOnly":"true", "f":"json"}

            dict =  fetch_json(source, params)
            if dict and "objectIds" in dict:
                if dict["objectIds"]:
                    return dict["objectIds"][0]

    def _get_landuse_vacancy(self):
        data = self.landuse_data
        if data:
            if data["C_DIG3"] == 911:
                return True
            else:
                return False

    def _get_availability(self):
        if self.papl_listing_id:
            return True
        else:
            return False
    
    def _get_public_status(self):
        if self.papl_asset_id:
            return True
        else:
            return False
    
    def _get_vacancy_status(self):
        #TODO
        pass

    @property
    def papl_listing_data(self):
        source = settings.PHL_DATA["PAPL_LISTINGS"] + str(self._get_papl_listing_id())
        params = {"f":"json"}

        data = fetch_json(source, params)
        
        if data and "feature" in data:
            return data["feature"]["attributes"]

    @property
    def papl_asset_data(self):
        source = settings.PHL_DATA["PAPL_LISTINGS"] + str(self._get_papl_asset_id())
        params = {"f":"json"}

        data = fetch_json(source, params)

        if data and "feature" in data:
            return data["feature"]["attributes"]

    @property
    def vacancy_license_data(self):
        source = settings.PHL_DATA["VACANCY_LICENSES"] + str(self._get_vacancy_license_id())
        params = {"f":"json"}

        data = fetch_json(source, params)

        if data and "feature" in data:
            return data["feature"]["attributes"]

    @property
    def vacancy_violation_data(self):
        source = settings.PHL_DATA["VACANCY_VIOLATIONS"] + str(self._get_vacancy_violation_id())
        params = {"f":"json"}

        data = fetch_json(source, params)

        if data and "feature" in data:
            return data["feature"]["attributes"]
    
    @property
    def demolition_data(self):
        source = settings.PHL_DATA["VACANCY_DEMOLITIONS"] + str(self._get_demolition_id())
        params = {"f":"json"}

        data = fetch_json(source, params)

        if data and "feature" in data:
            return data["feature"]["attributes"]

    @property
    def demolition_permit_data(self):
        source = settings.PHL_DATA["VACANCY_DEMOLITION_PERMITS"] + str(self._get_demolition_permit_id())
        params = {"f":"json"}

        data = fetch_json(source, params)

        if data and "feature" in data:
            return data["feature"]["attributes"]

    @property
    def landuse_data(self):
        id = self._get_landuse_id()
        source = settings.PHL_DATA["LAND_USE"] + str(id)
        params = {"f":"json"}

        data = fetch_json(source, params)

        if not "error" in data:
            if "feature" in data:
                return data["feature"]["attributes"]
    
    @property
    def address_data(self):
        address = self.address.replace (" ", "+")
        source = settings.PHL_DATA["ADDRESS_API"] + address
        params = {}

        data = fetch_json(source, params)

        if not "error" in data:
            if "property" in data:
                return data["property"]
    
    @property
    def vacancy_status(self):
        return self._get_vacancy_status()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # These are all lots for Philadelphia, PA.
            # So populate those fields on creation.
            self.city = "Philadelphia"
            self.state = "PA"
            # self.zip = self._get_zip()
            #self.coord = self._get_coordinates()
            #self.is_vacant = self._get_vacancy_status()
            #self.is_public = self._get_public_status()
            #self.is_available = self._get_availability()
            #self.has_vacancy_violation = self._get_vacancy_violation()
            #self.has_vacancy_license = self._get_vacancy_license()
        super(Lot, self).save(*args, **kwargs)

class Parcel(models.Model):
    # spatial queryset manager
    objects = models.GeoManager()


    # Fields mapped to the Philadelphia parcel shapefile
    objectid = models.IntegerField()
    recsub = models.CharField(max_length=2, null=True, blank=True,
                              help_text="Submap to a registry map")
    basereg = models.CharField(max_length=10, null=True, blank=True,
                               help_text="The registry number which there is a deed attached to")
    mapreg = models.CharField(max_length=10, null=True, blank=True,
                              help_text="Registry number that may or may not specifically have a deed " \
                                        "attached to it.  In cases of parcels crossing multiple maps see " \
                                        "the BASEREG for the associated deed.")
    parcel = models.CharField(max_length=4, null=True, blank=True,
                              help_text="identifier for properties on the same map.")
    recmap = models.CharField(max_length=6, null=True, blank=True,
                              help_text="registry map name.  Department of Records tax map.")
    stcod = models.IntegerField('Street Code', null=True, blank=True,
                                help_text="Street code.  Maintained by the City of Philadelphia-Department " \
                                          "of Streets")
    house = models.IntegerField('House Number', null=True, blank=True)
    suf = models.CharField('House Number Suffix', max_length=1, null=True, blank=True)
    unit = models.CharField('Address Unit', max_length=7, null=True, blank=True)
    stex = models.IntegerField('Address Extention', null=True, blank=True)
    stdir = models.CharField('Street Direction', max_length=254, null=True, blank=True)
    stnam = models.CharField('Street Name', max_length=30, null=True, blank=True)
    stdes = models.CharField('Street Designation', max_length=3, null=True, blank=True)
    stdessuf = models.CharField('Street Designation Suffix',max_length=1, null=True, blank=True)
    elev_flag = models.IntegerField('Elevation Flag', null=True, blank=True,
                                    help_text="Whether or not a parcel contains elevated rights")
    topelev = models.FloatField('Highest Elevation', null=True, blank=True)
    botelev = models.FloatField('Lowest Elevation', null=True, blank=True)
    condoflag = models.IntegerField('Condominium Flag', null=True, blank=True)
    matchflag = models.IntegerField(null=True, blank=True)
    inactdate = models.DateField('Inactivation Date', null=True, blank=True)
    orig_date = models.DateField('Origination Date', null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    geoid = models.CharField(max_length=25, null=True, blank=True)
    shape_area = models.FloatField(null=True, blank=True)
    shape_len = models.FloatField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, geography=True)

    def _get_address(self):
        _address_fields = (self.house, self.suf, self.unit, self.stex, self.stdir, self.stnam, self.stdes, self.stdessuf)
        address = " ".join(str(s) for s in _address_fields if s)
        if address:
            return address
        else:
            return "unknown"

    def __unicode__(self):
        return u'%s' % (self._get_address())


def parcel_post_save(sender, **kwargs):
    """
        When a parcel instance is created, create a related Lot instance.
        Then use its address data and geometry data to update the related
        Lot address and coord fields, respectively.
    """
    parcel, created = kwargs["instance"], kwargs["created"]
    # if this is a new instance of parcel, 
    # create and populate the related Lot
    if created:
        Lot.objects.create(parcel=parcel, address=parcel._get_address(),
            geom=parcel.geom)

#post_save.connect(parcel_post_save, sender=Parcel)


