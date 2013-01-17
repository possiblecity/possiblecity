from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from possiblecity.philadelphia.views import *
 
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="philadelphia/public.html"), 
        name='lotxlot'),

    url(r'^lots/lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),

    url(r'^geo/lots/lot/(?P<pk>\d+)/$', LotDetailMapView.as_view(), name='geo_lot_detail'),  
  
    url(r'^geo/lots/vacant/available/polygons/$', cache_page(AvailableLotPolyMapView.as_view(),60*60), 
        name='available_lots_polys'),
    
)
