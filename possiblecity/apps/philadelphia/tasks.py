# philadelphia/tasks.py

import os

from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from models import LotProfile

from celery import task

pwd_parcel_mapping = {
    'opa_code': 'TENCODE', 
    'brt_id': 'BRT_ID',
    'address': 'ADDRESS',
    'pwd_parcel': 'MULTIPOLYGON'
}

def _get_filepath(file):
    return os.path.abspath(os.path.join(settings.PROJECT_ROOT, 'data', file))

@task()
def map():
    data_source = _get_filepath('all_the_rest/pwd_parcels_all_the_rest.shp')
    lm = LayerMapping(LotProfile, data_source, pwd_parcel_mapping,
                      transform=False, encoding='iso-8859-1')
    lm.save(verbose=True, step=1000)

