# philadelphia/views.py

from django.contrib.gis.geos import Point, Polygon
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import *
from possiblecity.lotxlot.forms import AddressForm
from possiblecity.lotxlot.utils import fetch_json

from models import Lot

class LotDetailView(DetailView):
    """
    Retreive a lot
    """
    model = Lot    

# ajax views
class LotDetailMapView(GeoDetailView):
    model = Lot
    geo_field = "geom"

    
class LotListApiView(BBoxMixin, CallbackMixin, GeoListView):
    """
    Return all lot objects
    """
    model = Lot
    geo_field = "geom"
    properties = ['address', 'id', 'is_public', 'is_available']
   
class VacantLotListApiView(LotListApiView):
    """
    Return all vacant lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)

class VacantUnavailableLotListApiView(LotListApiView):
    """
    Return all lots not for sale
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True, is_available=False)
                 
class VacantAvailableLotListApiView(LotListApiView):
    """
    Return all vacant lots for sale
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True, is_available=True)

class PublicVacantLotListApiView(LotListApiView):
    """
    Return all vacant and public lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_public=True, is_visible=True)

class PrivateVacantLotListApiView(LotListApiView):
    """
    Return all vacant and public lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_public=False, is_visible=True)

class PublicAvailableVacantLotListApiView(LotListApiView):
    """
    Return all vacant and available lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_available=True, is_visible=True)

class PublicUnavailableVacantLotListApiView(LotListApiView):
    """
    Return all vacant and public lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_public=True, is_available=False, is_visible=True)

class PrivateUnverifiedVacantLotListApiView(LotListApiView):
    """
    Return all vacant lots that are not public, 
    and do not have a vacancy violation or vacancy license
    """
    queryset = Lot.objects.filter(is_visible=True, is_vacant=True,
                                  is_public=False, has_vacancy_license=False,
                                  has_vacancy_violation=False)

class PrivateVerifiedVacantLotListApiView(LotListApiView):
    """
    Return all vacant lots that are private and have a vacancy license 
    or a vacancy violation
    """
    queryset = Lot.objects.filter(is_visible=True, is_public=False)\
                          .filter(Q(has_vacancy_violation=True) | Q(has_vacancy_license=True))
   
    

class LotsNearAddress(AddressSearchView):
    queryset = Lot.objects.filter(is_vacant=True).filter(is_visible=True)
    template_name = 'philadelphia/search.html'
    geo_field = "geom"
    properties = ['address', 'id', 'is_public', 'is_available', 'is_vacant',
                  'has_vacancy_license', 'has_vacancy_violation', 'has_vacant_building']
    distance = 400
    default_origin = Point(-75.163894, 39.952247)






