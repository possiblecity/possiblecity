import os
from django.contrib.gis.utils import LayerMapping
from models import Parcel

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


parcels = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/parcels1.shp'))

test_parcels = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/test_parcels.shp'))

def _get_filepath(file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', file))

def map_parcels(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(Parcel, parcels, parcel_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

def map_parcels_test(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(Parcel, test_parcels, parcel_mapping,
        transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)


