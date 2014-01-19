# lotxlot/urls.py

from django.conf.urls import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import (LotDetailView, LotMapView, LotListView, LotListPublicView, 
	LotListPrivateView, LotListVacantView, LotListVacantPublicView, LotListVacantPrivateView)
 
urlpatterns = patterns('',
	url(r'^$', LotListView.as_view(), name='lotxlot_lot_list'),
	url(r'^$', LotListPublicView.as_view(), name='lotxlot_lot_list_public'),
	url(r'^$', LotListPrivateView.as_view(), name='lotxlot_lot_list_private'),

	url(r'^vacant/$', LotListVacantView.as_view(), name='lotxlot_lot_list_vacant'),
	url(r'^vacant/public/$', LotListVacantPublicView.as_view(), name='lotxlot_lot_list_vacant_public'),
	url(r'^vacant/private/$', LotListVacantPrivateView.as_view(), name='lotxlot_lot_list_vacant_private'),

    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),

    url(r'^map/$$', LotMapView.as_view(), name='lotxlot_map'),
)
