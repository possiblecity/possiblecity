# lotxlot/urls.py

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'lots', LotViewSet)
 
urlpatterns = patterns('',
    url(r'^lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),

    url(r'^api/v1/lots/lot/(?P<pk>\d+)/$', LotDetailMapView.as_view(), name='api_lot_detail'),
    url(r'^api/v1/lots/vacant/$', VacantLotListApiView.as_view(), name="api_lots_vacant"),
)
