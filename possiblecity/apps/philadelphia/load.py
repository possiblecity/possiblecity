import os
from django.contrib.gis.utils import LayerMapping
from models import Parcel

parcel_mapping = {
    'basereg' : 'BASEREG',
}

pwd_mapping = {
    'opa_code': 'TENCODE', 
    'address': 'ADDRESS',
    'shape': 'MULTIPOLYGON'
}

neighborhood_mapping = {
    'name' : 'NAME',
    'list_name' : 'LISTNAME',
    'map_name' : 'MAPNAME',
    'shape' : 'MULTIPOLYGON'
}


def _get_filepath(file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', file))

def map(model, data_source, mapping, verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(model, data_source, mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)

def map_parcels_test(verbose=True, strict=True, progress=False, step=False):
    lm = LayerMapping(Parcel, test_parcels, parcel_mapping,
        transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)


