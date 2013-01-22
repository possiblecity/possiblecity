# philadelphia/views.py

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView

from possiblecity.lotxlot.views import *
from possiblecity.lotxlot.forms import AddressForm
from possiblecity.lotxlot.utils import fetch_json
from possiblecity.philadelphia.models import Lot


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

class LotsNearAddress(AddressSearchView):
    queryset = Lot.objects.filter(is_vacant=True)
    geo_field = 'geom'
    template_name = 'philadelphia/search.html'
    point_field = 'coord'

def lots_near_address(request):
    form_class = AddressForm
    model = Lot
    template_name = 'philadelphia/search.html'

    form = form_class(request.POST or None)
    if form.is_valid():
        address = form.cleaned_data['address']
        coord = address['coord']
        lot_list = model.objects.filter(is_vacant=True).filter(coord__distance_lte=(coord, 400))
    else:
        lot_list = model.objects.filter(is_vacant=True).filter(is_public=True)

    return render_to_response(template_name, 
            {'form': form, 'lot_list': lot_list,}, 
            context_instance=RequestContext(request))











