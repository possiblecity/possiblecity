# lotxlot/views.py

from vectorformats.Formats import Django, GeoJSON

from django.http import HttpResponse
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView

class GeoResponseMixin(object):
    
    geo_field = "geom" # default value for the geometry field
    properties = [] # additional properties to add to result

    def render_to_response(self, context):
        qs = self.get_queryset()
        djf = Django.Django(geodjango=self.geo_field)
        geoj = GeoJSON.GeoJSON()
        output = geoj.encode(djf.decode(qs))
        return HttpResponse(output, content_type='application/json')


class GeoListView(GeoResponseMixin, BaseListView):
    pass

class GeoDetailView(BaseDetailView, GeoResponseMixin):
    def get_queryset(self):
        # GeoJSON expects a list
        return self.model._default_manager.filter(pk=self.kwargs['pk'])

class GeoHybridListView(GeoResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    """
    A generic model list view which  serves either GeoJSON or html 
    depending on the type of request
    """
    def render_to_response(self, context): 
        if self.request.GET.get('format','html') == 'json':
            return GeoResponseMixin.render_to_response(self, context)
        else:
            return MultipleObjectTemplateResponseMixin.render_to_response(self, context) 

class GeoHybridDetailView(GeoDetailView, SingleObjectTemplateResponseMixin):
    """
    A generic object detail view which serves either GeoJSON or html
    depending on the type of request
    """
    def render_to_response(self, context):
        if self.request.GET.get('format','html') == 'json':
            return GeoDetailView.render_to_response(self, context)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)
