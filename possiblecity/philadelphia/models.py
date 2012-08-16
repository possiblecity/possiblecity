# philadelphia/models.py
from django.contrib.gis.db import models
from django.db.models.signals import post_save

from possiblecity.lotxlot.models import USLotBase

class Lot(USLotBase):
    # spatial queryset manager
    objects = models.GeoManager()

    def _get_zip(self):
        # determine zip code from address, city and state
        pass

    def save(self, force_insert=False, force_update=False):
        if not self.pk:
            # These are all lots for Philadelphia, PA.
            # So populate those fields on creation.
            self.city = "Philadelphia"
            self.state = "PA"
            # self.zip = self._get_zip
        super(Lot, self).save(force_insert, force_update)

class Parcel(models.Model):
    # spatial queryset manager
    objects = models.GeoManager()

    lot = models.OneToOneField(Lot)

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
        _address_fields = (self.house, self.suf, self.unit, self.stex, self.stdir, self.stname, self.stdes, self.stdessuf)
        return " ".join(str(s) for s in _address_fields if s is not None)

    def _get_coordinates(self):
        # get coordinates from geom field
        return self.geom.centroid



# Auto-generated `LayerMapping` dictionary for Parcel model
parcel_mapping = {
    'objectid' : 'OBJECTID',
    'recsub' : 'RECSUB',
    'basereg' : 'BASEREG',
    'mapreg' : 'MAPREG',
    'parcel' : 'PARCEL',
    'recmap' : 'RECMAP',
    'stcod' : 'STCOD',
    'house' : 'HOUSE',
    'suf' : 'SUF',
    'unit' : 'UNIT',
    'stex' : 'STEX',
    'stdir' : 'STDIR',
    'stnam' : 'STNAM',
    'stdes' : 'STDES',
    'stdessuf' : 'STDESSUF',
    'elev_flag' : 'ELEV_FLAG',
    'topelev' : 'TOPELEV',
    'botelev' : 'BOTELEV',
    'condoflag' : 'CONDOFLAG',
    'matchflag' : 'MATCHFLAG',
    'inactdate' : 'INACTDATE',
    'orig_date' : 'ORIG_DATE',
    'status' : 'STATUS',
    'geoid' : 'GEOID',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'MULTIPOLYGON',
}

def parcel_post_save(sender, **kwargs):
    """
        When a parcel instance is created, create a related Lot instance.
        Then use its address data and geometry data to update the related
        Lot address and coord fields, respectively.
    """
    parcel, created = kwargs["instance"], kwargs["created"]
    # if this is a new instance of parcel, create a populate a related Lot
    if created:
        # create the Lot instance
        lot = Lot(parcel=parcel, address=parcel._get_address,
                  coord=parcel._get_coordinates, geom=parcel.geom)
        lot.save()

post_save.connect(parcel_post_save, sender=Parcel)
