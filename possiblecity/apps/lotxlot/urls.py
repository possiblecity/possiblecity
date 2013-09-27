# lotxlot/urls.py

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import LotDetailView, LotIndexView, LotOrNotListView, LotOrNotSizeAscListView
 
urlpatterns = patterns('',
	url(r'^$', LotIndexView.as_view(), name='lotxlot'),
    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),
    url(r'^lotornot/$', LotOrNotListView.as_view(), name='lot_or_not'),
    url(r'^lotornot/asc', LotOrNotSizeAscListView.as_view(), name='lot_or_not_size_asc'),
)
