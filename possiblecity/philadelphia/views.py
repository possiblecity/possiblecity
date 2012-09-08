# philadelphia/views.py

from django.http import HttpResponse
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import GeoHybridListView, GeoHybridDetailView
from possiblecity.philadelphia.models import Lot

class LotListView(GeoHybridListView):
    """
    Retrieve all lots.
    """
    model = Lot
    geodjango = "coord"

class LotDetailView(GeoHybridDetailView):
    """
    Retreive a lot
    """
    model = Lot
    geodjango = "geom"
    

