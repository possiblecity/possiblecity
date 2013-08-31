# lotxlot/views.py

from vectorformats.Formats import Django, GeoJSON

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point, Polygon
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView
from django.views.generic.edit import FormMixin

from braces.views import CanonicalSlugDetailMixin, LoginRequiredMixin
from extra_views import InlineFormSetView


from apps.ideas.models import Idea

from .forms import AddressForm, LotForm, IdeaInlineFormSet
from .models import Lot
from .utils import fetch_json


 
##### GENERIC MIXINS
class GeoResponseMixin(object):
    """
    A mixin that returns a geojson geometry field for each object in the queryset. 
    The field can be configured with the "geo_field" class property. 
    Additional fields from the model can be included using the "properties" list.
    """
    geo_field = "geom" # default value for the geometry field
    properties = [] # additional properties to add to result

    def encode_queryset(self):
        qs = self.get_queryset()
        djf = Django.Django(geodjango=self.geo_field, properties=self.properties)
        geoj = GeoJSON.GeoJSON()
        return geoj.encode(djf.decode(qs))

    def render_to_response(self, context):
        output = self.encode_queryset()
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

class BBoxMixin(object):
    bounds = None
    def get_queryset(self):
        queryset = super(BBoxMixin, self).get_queryset()
        if self.request.GET.get('bbox'):      
            bbox = self.request.GET.get('bbox')
            bbox = tuple(bbox.split(","))
            bounds = Polygon.from_bbox(bbox)
            # return a filtered queryset
            queryset = queryset.filter(coord__within=bounds)
        return queryset
       
class CallbackMixin(object):
    def encode_queryset(self):
        callback = self.request.GET.get('callback')
        output = super(CallbackMixin, self).encode_queryset()
        if callback:
            output = callback + '(' + output + ');'
        return output

class LocationSearchMixin(object):
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
            filter = point_field + '__' + search_type
           
            # Fetch the queryset from the parent's get_queryset
            queryset = super(LocationSearchView, self).get_queryset() 
            # return a filtered queryset           
            return queryset.filter(**{ filter: (origin, distance)})

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

class AddressSearchView(FormMixin, MultipleObjectMixin, HybridGeoResponseMixin, View):
    """
    A View which takes a queryset and filters it via a form submission
    """
    form_class = AddressForm
    distance = 400
    default_origin = None

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None: 
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                        % self.__class__.__name__)
        queryset = queryset.filter(coord__distance_lte=(self.default_origin, self.distance))
        return queryset

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        object_list = self.get_queryset()
        origin = self.default_origin
        context = self.get_context_data(object_list=object_list, form=form, origin=origin)
        return self.render_to_response(context) 
        
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            origin = form.cleaned_data['address']
        else:
            origin = self.default_origin
        object_list = self.get_queryset().filter(coord__distance_lte=(origin, self.distance))
        context = self.get_context_data(object_list=object_list, form=form, origin=origin)
        return self.render_to_response(context) 


# ajax views
class LotDetailMapView(GeoDetailView):
    model = Lot
    geo_field = "bounds"

    
class LotListApiView(BBoxMixin, CallbackMixin, GeoListView):
    """
    Return all lot objects
    """
    model = Lot
    geo_field = "bounds"
    properties = ['address', 'id', 'is_public', 'slug']
   
class VacantLotListApiView(LotListApiView):
    """
    Return all vacant lot objects
    """
    queryset = Lot.objects.filter(is_vacant=True, is_visible=True)


class LotDetailView(UpdateView):
    model=Lot
    template_name = 'lotxlot/lot_detail.html'

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            self.request.session['post'] = self.request.POST
            url = "%s?next=%s" % (reverse('account_login'), request.path)
            return HttpResponseRedirect(url)
        else:
            return super(LotDetailView, self).post(request, *args, **kwargs)

    def formset_valid(self, formset):
        """
        Auto-populate user
       and save form.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = self.request.user
            instance.save()

        return HttpResponseRedirect(self.get_success_url())

#class LotDetailView(InlineFormSetView):
#    model = Lot
#    inline_model = Idea.lots.through.idea
#    formset_class = IdeaInlineFormSet
#    can_delete = False
#    extra = 1
#    template_name = 'lotxlot/lot_detail.html'

#    def post(self, request, *args, **kwargs):
#        if not self.request.user.is_authenticated():
#            self.request.session['post'] = self.request.POST
#            url = "%s?next=%s" % (reverse('account_login'), request.path)
#            return HttpResponseRedirect(url)
#        else:
#            return super(LotDetailView, self).post(request, *args, **kwargs)

#    def formset_valid(self, formset):
#        """
#        Auto-populate user
#       and save form.
#        """
#        instances = formset.save(commit=False)
#        for instance in instances:
#            instance.user = self.request.user
#            instance.save()

#        return HttpResponseRedirect(self.get_success_url())







