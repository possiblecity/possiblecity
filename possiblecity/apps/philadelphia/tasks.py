# philadelphia/tasks.py

import datetime
import os

import json
import requests

from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from models import LotProfile

from celery import task

from apps.lotxlot.utils import queryset_iterator

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
                      transform=False, encoding='iso-8859-1', unique='TENCODE')
    lm.save(verbose=True, step=1000)


@task()
def check_landuse_vacancy():
    """
    Check landuse data source to get vacancy status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    t = datetime.datetime.now() - datetime.timedelta(days=1)
    queryset = queryset_iterator(Lot.objects.filter(created__gt=t))
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["LAND_USE"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        req = requests.get(source, params=params)

        data = json.loads(req.text)

        if data:
            if "features" in data:
                features = data["features"]
                if features[0]:
                    attributes = features[0]["attributes"]
                    if "C_DIG3" in attributes:
                        if attributes["C_DIG3"] == 911:
                            lot.is_vacant = True
                            lot.save(update_fields=["is_vacant",])
                            print("updated lot %s") % lot.address
        else:
            print(lot.id)                                

@task()
def check_public():
    """
    Check papl assets data source to get public status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    t = datetime.datetime.now() - datetime.timedelta(days=1)
    queryset = queryset_iterator(Lot.objects.vacant())
    #queryset = queryset_iterator(Lot.objects.filter(created__gt=t))
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["PAPL_ASSETS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        req = requests.get(source, params=params)
	data = json.loads(req.text)

        if data:
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        lot.is_public = True
                        lot.save(update_fields=["is_public",])
                        print("updated lot %s") % lot.address
                        

@task()    
def get_basereg():
    """
    Check papl parcel data source to get basereg number.
    Update database accordingly.
    """
    from .models import LotProfile

    queryset = queryset_iterator(LotProfile.objects.filter(basereg=''))
    for lot_profile in queryset:
        lon = lot_profile.get_center().x
        lat = lot_profile.get_center().y
        source = settings.PHL_DATA["PAPL_PARCELS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"BASEREG", "f":"json"}

        req = requests.get(source, params=params)

        data = json.loads(req.text)

        if data:
            if "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        attributes = features[0]["attributes"]
                        lot_profile.basereg = attributes["BASEREG"]
                        lot_profile.save(update_fields=["basereg",])
                        print("updated lot %s") % lot_profile.address

@task 
def update_vacancy(public=False):
     """
     Check vacancy indicators and mark is_vacant 
     appropriately
     """
     from apps.lotxlot.models import Lot

     t = datetime.datetime.now() - datetime.timedelta(days=14) 
     if public:
         queryset = queryset_iterator(Lot.objects.public())
     else:
         queryset = queryset_iterator(Lot.objects.filter(is_vacant=False, updated__lt=t))
     for lot in queryset:
         vacant = lot.is_vacant
         if lot.profile.is_bldg_desc_vacant:
             vacant=True
             indicator="bldg desc"
         elif lot.profile.is_land_use_vacant:
             vacant=True
             indicator="land use"
         elif lot.profile.has_license:
             vacant=True
             indicator="license"
         elif lot.profile.has_violation:
             vacant=True
             indicator="violation"
         elif lot.profile.is_for_sale:
             vacant=True
             indicator="for sale"
         else:
             vacant=False
             indicator="Not Vacant"

         lot.is_vacant = vacant
         lot.save(update_fields=["is_vacant", "updated"])
         print("updated lot %s: %s") % (lot.id, indicator)
         
