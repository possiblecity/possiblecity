import os
from django.contrib.gis.utils import LayerMapping
from models import Parcel, LandUnit

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

parcels = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/PhiladelphiaParcels201201.shp'))

test_parcels = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/parcel_test.shp'))

land_use = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/vacant_parcels_WGS84.shp'))

def map_parcels(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(Parcel, shp, parcel_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

def map_parcel_test(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(Parcel, test_parcels, parcel_mapping,
        transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

def map_landuse(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(LandUnit, land_use, land_mapping,
        transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

