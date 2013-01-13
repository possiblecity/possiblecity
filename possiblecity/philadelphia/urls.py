from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from possiblecity.philadelphia.views import *
 
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="philadelphia/public.html"), 
        name='lotxlot'),
        
    #url(r'^hexagons/$', TemplateView.as_view(template_name="philadelphia/hexbin.html"), 
    #    name='hexagons'),
        
    #url(r'^lots/$', LotListView.as_view(), name='lots'),
    #url(r'^lots/vacant/$', VacantLotListView.as_view(), name='vacant_lots'),
    #url(r'^lots/area/$', LotsByAreaView.as_view(), name='lots_by_area'),
    
    url(r'^lots/lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),
    
    #url(r'^geo/lots/vacant/points/$', VacantLotMapView.as_view(), 
    #    name='vacant_lots_points'),
    #url(r'^geo/lots/vacant/polygons/$', VacantLotPolyMapView.as_view(), 
    #    name='vacant_lots_polys'), 
    #url(r'^geo/lots/vacant/available/points/$', AvailableLotMapView.as_view(), 
    #    name='available_lots_points'),
    
    url(r'^geo/lots/vacant/available/polygons/$', AvailableLotPolyMapView.as_view(), 
        name='available_lots_polys'),
    
    #url(r'^geo/lots/vacant/unavailable/points/$', UnavailablePublicVacantLotMapView.as_view(), 
    #    name='unavailable_lots_points'),
    #url(r'^geo/lots/vacant/unavailable/polygons/$', UnavailablePublicVacantLotPolyMapView.as_view(), 
        name='unavailable_lots_polys'),
    #url(r'^geo/lots/vacant/private/points/$', PrivateVacantLotMapView.as_view(), 
    #    name='private_lots_points'),
    #url(r'^geo/lots/vacant/private/polygons/$', PrivateVacantLotPolyMapView.as_view(), 
    #    name='private_lots_polys'),
)
