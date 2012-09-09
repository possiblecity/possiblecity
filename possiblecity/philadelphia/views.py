# philadelphia/views.py

from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import GeoListView, GeoHybridListView, GeoHybridDetailView
from possiblecity.philadelphia.models import Lot

class LotListView(GeoHybridListView):
    """
    Retrieve all lots.
    """
    queryset = Lot.objects.filter(is_visible=True)
    geo_field = "coord"

class VacantLotListView(GeoHybridListView):
    """
    Retrieve all vacant lots
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)
    template_name = "philadelphia/lot_list.html"
    geo_field = "geom"
    

class PublicLotListView(GeoHybridListView):
    """
    Retrieve all public lots
    """
    queryset = Lot.objects.filter(is_public=True, is_visible=True)
    template_name = "philadelphia/lot_list.html"
    geo_field = "geom"

class VacantPublicLotListView(GeoHybridListView):
    """
    Retrieve all vacant public lots
    """
    queryset = Lot.objects.filter(is_vacant=True, is_public=True, is_visible=True)
    template_name = "philadelphia/lot_list.html"
    geo_field = "geom"

class VacantPrivateLotListView(GeoHybridListView):
   """
   Retrieve all vacant private lots
   """
   queryset = Lot.objects.filter(is_vacant=True, is_public=False, is_visible=True)  
   template_name = "philadelphia/lot_list.html"
   geo_field = "geom"
    

class VacantAvailableLotListView(GeoHybridListView):
    """
    Retrieve all vacant lots for sale
    """
    queryset = Lot.objects.filter(is_available=True, is_visible=True)
    template_name = "philadelphia/lot_list.html"
    geo_field = "geom"


class LotsByAreaView(GeoHybridListView):
    """
    Retrieve all lots sorted by area
    """
    queryset = Lot.objects.filter(is_visible=True).order_by('parcel__shape_area')
    template_name = 'philadelphia/lot_list.html'
    geo_field = "coord"

class VacantLotsByAreaView(GeoHybridListView):
    """
    Retrieve all vacant lots sorted by area
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True).order_by('parcel__shape_area')
    template_name = "philadelphia/lot_list.html"

    geo_field = "geom"

class LotDetailView(GeoHybridDetailView):
    """
    Retreive a lot
    """
    model = Lot
    geo_field = "geom"
    

