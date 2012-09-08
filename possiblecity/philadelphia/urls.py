from django.conf.urls.defaults import *
 
from possiblecity.philadelphia.views import LotListView, LotDetailView
 
urlpatterns = patterns('',
    url(r'^lots/$', LotListView.as_view(), name='lots'),
    url(r'^lots/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),
)
