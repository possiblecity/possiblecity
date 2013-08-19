import os
from django.contrib.gis.utils import LayerMapping
from models import LotProfile, Neighborhood

dor_parcel_mapping = {
    'basereg' : 'BASEREG',
}

pwd_parcel_mapping = {
    'opa_code': 'TENCODE', 
    'address': 'ADDRESS',
    'pwd_parcel': 'MULTIPOLYGON'
}

neighborhood_mapping = {
    'name': 'NAME',
    'map_name': 'MAPNAME',
    'list_name': 'LISTNAME',
    'bounds': 'MULTIPOLYGON'
}

point_breeze = 'point_breeze/point_breeze_pwd_parcels.shp'
neighborhoods = 'Neighborhoods_Philadelphia/neighborhoods_philadelphia.shp'


def _get_filepath(file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', file))

def map(model, file, mapping, verbose=True, strict=True, progress=False, step=False):
    data_source = _get_filepath(file)
    lm = LayerMapping(model, data_source, mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=verbose, strict=strict, progress=progress, step=step)


