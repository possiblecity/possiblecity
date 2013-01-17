# philadelphia/views.py

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import *
from possiblecity.lotxlot.utils import fetch_json
from possiblecity.philadelphia.models import Lot

# ajax views
class LotDetailMapView(GeoDetailView):
    model = Lot
    geo_field = "geom"

class LotListMapView(GeoListView):
    properties = ['address', 'id', 'is_public']

class VacantLotMapView(LotListMapView):
    # return geojson coordinates to display on a map
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)
    geo_field = "coord"
   
class VacantLotPolyMapView(VacantLotMapView):
    # return geojson polygons to display on a map
    geo_field = "geom"
   
class AvailableLotMapView(LotListMapView):
    # return geojson coordinates to display on a map
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True, is_available=True)
    geo_field = "coord"

class AvailableLotPolyMapView(AvailableLotMapView):
    # return geojson polygons to display on a map
    geo_field = "geom"
    
class UnavailablePublicVacantLotMapView(LotListMapView):
    # return geojson coordinates to display on a map
    queryset = Lot.objects.filter(is_visible=True, is_vacant=True, is_public=True, is_available=False)
    geo_field = "coord"
    
class UnavailablePublicVacantLotPolyMapView(UnavailablePublicVacantLotMapView):
    geo_field = "geom"
    
class PrivateVacantLotMapView(LotListMapView):
    queryset = Lot.objects.filter(is_visible=True, is_vacant=True, is_public=False)
    geo_field = "coord"

class PrivateVacantLotPolyMapView(PrivateVacantLotMapView):
    geo_field = "geom"


# hybrid views
class LotListView(GeoHybridListView):
    """
    Retrieve all lots.
    """
    queryset = Lot.objects.filter(is_visible=True)
    template_name = "philadelphia/lot_list.html"
    paginate_by = 10
    geo_field = "coord"

class VacantLotListView(LotListView):
    """
    Retrieve all vacant lots
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)
    
class PublicLotListView(LotListView):
    """
    Retrieve all public lots
    """
    queryset = Lot.objects.filter(is_public=True, is_visible=True)
    
class VacantPublicLotListView(LotListView):
    """
    Retrieve all vacant public lots
    """
    queryset = Lot.objects.filter(is_vacant=True, is_public=True, is_visible=True)

class VacantPrivateLotListView(LotListView):
   """
   Retrieve all vacant private lots
   """
   queryset = Lot.objects.filter(is_vacant=True, is_public=False, is_visible=True)
    
class VacantAvailableLotListView(LotListView):
    """
    Retrieve all vacant lots for sale
    """
    queryset = Lot.objects.filter(is_available=True, is_visible=True)


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




class LotDetailView(DetailView):
    """
    Retreive a lot
    """
    model = Lot
    
    def get_object(self):
        # Call the superclass
        object = super(LotDetailView, self).get_object()
        # refresh data sources
        object.update_availability()
        object.update_public_status()
        object.update_vacancy_status()
        object.save()
        # Return the object
        return object
    

