# philadelphia/models.py
from django.contrib.gis.db import models
from django.db.models import signals

from possiblecity.lotxlot.models import LotBase

class Lot(LotBase):
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
    # Already defined in LotBase
    # geom = models.MultiPolygonField(srid=4326, geography=True)

    def _get_address(self):
        _address_fields = (self.house, self.suf, self.unit, self.stex, self.stdir, self.stname, self.stdes, self.stdessuf)
        return " ".join(str(s) for s in _address_fields if s is not None)

    def _get_coordinates(self):
        # get coordinates from geom field
        return self.geom.centroid

    def save(self, force_insert=False, force_update=False):
        if not self.pk:
            # These are all lots for Philadelphia, PA. So populate those fields on creation.
            self.city = "Philadelphia"
            self.state = "PA"
            # populate address field with concatenation of address related fields from Parcel
            self.address = _get_address(self)
            # get coordinates from geometry
            self.coord = _get_coordinates(self)
        super(Lot, self).save(force_insert, force_update)

class LandUnit(models.Model):
    """
     Fields mapped to Philadelphia land use shape file
    """
    lot = models.ForeignKey(Lot, null=True, blank=True)

    # spatial queryset manager
    objects = models.GeoManager()

    # fields from Philadelphia City Planning shapefile for landuse
    objectid = models.IntegerField()
    c_dig1 = models.IntegerField()
    c_dig1desc = models.CharField(max_length=50)
    c_dig2 = models.IntegerField()
    c_dig2desc = models.CharField(max_length=50)
    c_dig3 = models.IntegerField()
    c_dig3desc = models.CharField(max_length=250)
    lu_current = models.IntegerField()
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.MultiPolygonField(srid=4326, geography=True)

class PhlPublicVacantLot(models.Model):
    """
        This model represents fields from an excel file release by the
        City of Philadelphia. It contains all of the publicly owned
        vacant property as of its release date on May 1, 2009.
    """
    zip_code = models.IntegerField()
    location = models.CharField(max_length=100)
    owner1 = models.CharField(max_length=100)
    owner2 = models.CharField(max_length=100)
    bldg_code = models.CharField(max_length=5)
    total_area = models.IntegerField()
    livable_area = models.IntegerField()
    recording_date = models.DateField()
    brief_descr = models.CharField(max_length=100)
    std_owner = models.CharField(max_length=100)
    abbr = models.CharField(max_length=100)
    market_value = models.DecimalField(max_digits=11, decimal_places=2)
    market_value_date = models.DateField()
    last_sale_price = models.DecimalField(max_digits=11, decimal_places=2)
    last_sale_date = models.DateField()
    taxable_land_value =  models.DecimalField(max_digits=11, decimal_places=2)
    taxable_building_value = models.DecimalField(max_digits=11, decimal_places=2)
    exempt_land_value = models.DecimalField(max_digits=11, decimal_places=2)
    exempt_building_value = models.DecimalField(max_digits=11, decimal_places=2)

    coord = models.PointField(blank=True, null=True)




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

# Auto-generated `LayerMapping` dictionary for LandUnit model
land_mapping = {
    'objectid' : 'OBJECTID',
    'c_dig1' : 'C_DIG1',
    'c_dig1desc' : 'C_DIG1DESC',
    'c_dig2' : 'C_DIG2',
    'c_dig2desc' : 'C_DIG2DESC',
    'c_dig3' : 'C_DIG3',
    'c_dig3desc' : 'C_DIG3DESC',
    'lu_current' : 'LU_CURRENT',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'MULTIPOLYGON',
}