# philadelphia/urls.py

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from possiblecity.philadelphia.views import *
 
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='philadelphia/vacant.html'), 
        name='lotxlot'),

    url(r'^lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),

    url(r'^api/v1/lots/vacant/$', VacantLotListApiView.as_view(), name="api_lots_vacant"),
    url(r'^api/v1/lots/vacant/available/$', VacantAvailableLotListApiView.as_view(), name="api_lots_vacant_available"),
    url(r'^api/v1/lots/vacant/unavailable/$', VacantUnavailableLotListApiView.as_view(), name="api_lots_vacant_unavailable"),
    url(r'^api/v1/lots/vacant/public/$', PublicVacantLotListApiView.as_view(), name="api_lots_vacant_public"),
    url(r'^api/v1/lots/vacant/public/available/$', PublicAvailableVacantLotListApiView.as_view(), name="api_lots_vacant_public_available"),
    #url(r'^api/v1/lots/vacant/private/verified/$', PrivateVerifiedVacantLotListApiView.as_view(), name="api_lots_vacant_private_verified"),
    #url(r'^api/v1/lots/vacant/private/unverified/$', PrivateUnverifiedLotListApiView.as_view(), name="api_lots_vacant_private_unverified"),

    url(r'^api/v1/lots/lot/(?P<pk>\d+)/$', LotDetailMapView.as_view(), name='api_lot_detail'),  
      
)
