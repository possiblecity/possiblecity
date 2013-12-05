# lotxlot/urls.py

from django.conf.urls import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import LotDetailView, LotIndexView, LotListView, LotListVacantView
 
urlpatterns = patterns('',
	url(r'^$', LotIndexView.as_view(), name='lotxlot'),
	url(r'^all/$', LotListView.as_view(), name='lotxlot_lot_list'),
	url(r'^vacant/$', LotListVacantView.as_view(), name='lotxlot_lot_list_vacant'),
    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),
)
