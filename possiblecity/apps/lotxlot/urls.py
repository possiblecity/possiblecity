# lotxlot/urls.py

from django.conf.urls import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import LotDetailView, LotMapView, LotListView, LotListVacantView
 
urlpatterns = patterns('',
	url(r'^$', LotListView.as_view(), name='lotxlot_lot_list'),
	url(r'^map/$$', LotMapView.as_view(), name='lotxlot_map'),
	url(r'^vacant/$', LotListVacantView.as_view(), name='lotxlot_lot_list_vacant'),
	url(r'^vacant/public/$', LotListVacantPublicView.as_view(), name='lotxlot_lot_list_vacant_public'),
	url(r'^vacant/private/$', LotListVacantPublicView.as_view(), name='lotxlot_lot_list_vacant_private'),
    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),
)
