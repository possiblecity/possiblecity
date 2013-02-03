# philadelphia/views.py

from django.contrib.gis.geos import Point, Polygon
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import *
from possiblecity.lotxlot.forms import AddressForm
from possiblecity.lotxlot.utils import fetch_json

from .models import Lot

class LotDetailView(DetailView):
    """
    Retrieve a lot
    """
    model = Lot
    
    def get_object(self):
        # Call the superclass
        object = super(LotDetailView, self).get_object()
        # refresh data sources
        object.update_availability()
        object.update_public_status()
        #object.update_vacancy_status()
        object.save()
        # Return the object
        return object

class LotDetailMapView(GeoDetailView):
    model = Lot
    geo_field = "geom"
    
class LotListView(HybridListView):
    """
    Return all lot objects
    """
    model = Lot
    geo_field = "geom"
    properties = ['address', 'id', 'is_public']
   
class AvailableVacantLotListView(LotListView):
    """
    Return all vacant and available lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_available=True, is_visible=True)

class VacantLotListView(LotListView):
    """
    Return all vacant lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)

class LotsNearAddress(AddressSearchView):
    queryset = Lot.objects.filter(is_vacant=True).filter(is_visible=True)
    template_name = 'philadelphia/search.html'
    geo_field = "geom"
    properties = ['address', 'id', 'is_public', 'is_available', 'is_vacant',
                  'has_vacancy_license', 'has_vacancy_violation', 'has_vacant_building']
    distance = 400
    default_origin = Point(-75.163894, 39.952247)

class BoundingBoxMixin(object):
    bounds = None
    def get_queryset(self):
        bbox = self.request.GET.get('bbox')
        bbox = tuple(bbox.split(","))
        bounds = Polygon.from_bbox(bbox)
	    # Fetch the queryset from the parent's get_queryset
        queryset = super(BoundingBoxMixin, self).get_queryset()
        # return a filtered queryset
        return queryset.filter(coord__within=bounds)

class BoundingBoxVacantLotSearch(BoundingBoxMixin, VacantLotListView):
    template_name = 'philadelphia/locate.html'
    




