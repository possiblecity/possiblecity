# philadelphia/models.py

from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_save

from possiblecity.lotxlot.utils import fetch_json, has_feature
from possiblecity.lotxlot.models import USLotBase

class Lot(USLotBase):
    # spatial queryset manager
    objects = models.GeoManager()
     
    parcel = models.OneToOneField("Parcel")

    is_available = models.BooleanField(default=False)
    has_vacancy_violation = models.BooleanField(default=False)
    has_vacancy_license = models.BooleanField(default=False)

    def _get_coordinates(self):
        # get coordinates from geom field
        return self.geom.centroid

    def _get_zip(self):
        # determine zip code from address, city and state
        pass

    def _get_vacancy_violation(self):
        source = settings.PHL_DATA["VACANCY_VIOLATIONS"] + "query"
        params = {"where":"VIOLATION_ADDRESS='%s'" % (self.address), "f":"json"}
        
        return has_feature(source, params)
   
    def _get_vacancy_license(self):
        source = settings.PHL_DATA["VACANCY_LICENSES"] + "query"
        params = {"where":"LICENSE_ADDRESS='%s'" % (self.address), "f":"json"}
        
        return has_feature(source, params)

    def _get_availability(self):
        source = settings.PHL_DATA["PAPL_LISTINGS"] + "query"
        params = {"where":"MAPREG='%s'" % (self.parcel.mapreg), "f":"json"}

        return has_feature(source, params)

    def _get_vacancy_status(self):
       vacancy_flags = (self._get_vacancy_violation(),
           self._get_vacancy_license(), self._get_availability())
       
       return any(v is True for v in vacancy_flags)
    
    def _get_public_status(self):
        source = settings.PHL_DATA["PAPL_ASSETS"] + "query"
        params = {"where":"MAPREG='%s'" % (self.parcel.mapreg), "f":"json"}

        return has_feature(source, params)

    def _get_listing_id(self):
        address = self.address.title()
        source = settings.PHL_DATA["PAPL_LISTINGS"] + "query"
        params = {"where":"REF_ADDRES='%s'" % (address), "returnIdsOnly":"true", "f":"json"}

        dict =  fetch_json(source, params)
        
        if dict["objectIds"]:
            if dict["objectIds"][0]:
                return dict["objectIds"][0]

    @property
    def papl_data(self):
        source = settings.PHL_DATA["PAPL_LISTINGS"] + str(self._get_listing_id())
        params = {"f":"json"}

        data = fetch_json(source, params)
        
        if not data["error"]:
            return data['feature']['attributes']

    def save(self, *args, **kwargs):
        if not self.pk:
            # These are all lots for Philadelphia, PA.
            # So populate those fields on creation.
            self.city = "Philadelphia"
            self.state = "PA"
            # self.zip = self._get_zip()
            self.coord = self._get_coordinates()
            self.is_vacant = self._get_vacancy_status()
            self.is_public = self._get_public_status()
            self.is_available = self._get_availability()
            self.has_vacancy_violation = self._get_vacancy_violation()
            self.has_vacancy_license = self._get_vacancy_license()
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
    geom = models.MultiPolygonField(srid=4326)

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

post_save.connect(parcel_post_save, sender=Parcel)
