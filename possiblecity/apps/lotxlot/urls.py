# lotxlot/urls.py

from django.conf.urls import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import LotDetailView, LotIndexView
 
urlpatterns = patterns('',
	url(r'^$', LotIndexView.as_view(), name='lotxlot'),
    url(r'^(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),
)
