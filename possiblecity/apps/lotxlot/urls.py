# lotxlot/urls.py

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import *
 
urlpatterns = patterns('',
    url(r'^lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lotxlot_lot_detail'),
)
