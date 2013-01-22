# lotxlot/views.py

from vectorformats.Formats import Django, GeoJSON

from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.views.generic.base import View, TemplateResponseMixinfrom django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView
from django.views.generic.edit import FormMixin

##### GENERIC MIXINS
class GeoResponseMixin(object):
    """
    A mixin that returns a geojson geometry field for each object in the queryset. 
    The field can be configured with the "geo_field" class property. 
    Additional fields from the model can be included using the "properties" list.
    """
    geo_field = "geom" # default value for the geometry field
    properties = [] # additional properties to add to result

    def render_to_response(self, context):
        qs = self.get_queryset()
        djf = Django.Django(geodjango=self.geo_field, properties=self.properties)
        geoj = GeoJSON.GeoJSON()
        output = geoj.encode(djf.decode(qs))
        return HttpResponse(output, content_type='application/json')

class HybridGeoResponseMixin(GeoResponseMixin, TemplateResponseMixin):
    """
    A mixin that returns either a geojson response, or a template response,
    depending on the format set in the url string. 
    """
    def render_to_response(self, context): 
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return GeoResponseMixin.render_to_response(self, context)
        else:
            return TemplateResponseMixin.render_to_response(self, context) 

### query filter mixins
class VacantMixin(object):
    """ 
    Filter for objects marked as vacant
    """
    def get_queryset(self):        # Fetch the queryset from the parent's get_queryset        queryset = super(VacantMixin, self).get_queryset()        # return a filtered queryset        return queryset.filter(is_vacant=True)

class PublicMixin(object):    
    """
    Filter for objects marked as public
    """
    def get_queryset(self):        # Fetch the queryset from the parent's get_queryset        queryset = super(VacantMixin, self).get_queryset()        # return a filtered queryset        return queryset.filter(is_public=True)

class VacantPublicMixin(object):
    """
    Filter for objects marked as vacant and pubic
    """
    def get_queryset(self):
        # Fetch the queryset from the parent's get_queryset        queryset = super(VacantMixin, self).get_queryset()        # return a filtered queryset        return queryset.filter(is_vacant=True).filter(is_public=True)class LocationSearchMixin(object):
    """
    A mixin that will filter a queryset based on each objects distance from a given origin.
    """
    # search defaults
    point_field = None # point field of objects to compare
    search_type = 'distance_lte' # defaults to less than or equal to
    origin = None # default search center point   
    distance = 400 # default search radius in meters 

    def get_queryset(self):
        if point_field is None:
            raise ImproperlyConfigured("You must supply a point field to compare to.")
        elif origin is None:
            raise ImproperlyConfigured("You must supply an origin point for your search.") 
        else:
            # build the filter parameters
            filter = point_field + '__' + search_type            # Fetch the queryset from the parent's get_queryset            queryset = super(LocationSearchView, self).get_queryset()            # return a filtered queryset            return queryset.filter(**{ filter: (origin, distance)})
    
##### GENERIC AJAX VIEWS
class GeoListView(GeoResponseMixin, BaseListView):
    """
    Returns a list of objects as geojson.
    
    Configurable properties and defaults:

    From GeoResponseMixin:
    geo_field = geom
    properties = []

    From MulitpleObjectMixin:
    allow_empty = True
    queryset = None
    model = None
    paginate_by = None
    context_object_name = None
    paginator_class = Paginator
    """
    pass

class GeoDetailView(GeoResponseMixin, BaseDetailView):
    """
    Returns a single object as geojson.
    
    Configurable properties and defaults:
    From GeoResponseMixin:
    geo_field = geom
    properties = []

    From SingleObjectMixin:
    model = None
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    """

    def get_queryset(self):
        # GeoJSON expects a list
        return self.model._default_manager.filter(pk=self.kwargs['pk'])


##### GENERIC HYBRID VIEWS
class HybridListView(HybridGeoResponseMixin, BaseListView):
    """
    A generic model list view which  serves either GeoJSON or html 
    depending on the type of request. Unlike ListView, you must explicitly specify
    the template name.
    """
    pass
     
class HybridDetailView(HybridGeoResponseMixin, BaseDetailView):
    """
    A generic object detail view which serves either GeoJSON or html
    depending on the type of request. Unlike DetailView, you must explicitly
    specify the template name.
    """
    pass

class AddressSearchView(FormMixin, MultipleObjectMixin, LocationSearchMixin, GeoResponseMixin, View):
    """
    Allow user to input a location. Use this location as an origin point to find
    objects within a certain distance.

    queryset = None
    geo_field = None
    form_class = AddressForm
    template_name = None
    point_field = None # point field of objects to compare
    search_type = 'distance_lte' # defaults to less than or equal to
    origin = None # default search center point   
    distance = 400 # default search radius in meters
    """  
   
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)    

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.origin = form.cleaned_data('address')
        return self.render_to_response()


     