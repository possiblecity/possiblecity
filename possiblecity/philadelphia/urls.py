from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from possiblecity.philadelphia.views import LotListView, LotDetailView, LotsByAreaView, VacantLotListView
 
urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='philadelphia/index.html')),
    url(r'^lots/$', LotListView.as_view(), name='lots'),
    url(r'^lots/vacant/$', VacantLotListView.as_view(), name='vacant_lots'),
    url(r'^lots/area/$', LotsByAreaView.as_view(), name='lots_by_area'),
    url(r'^lots/lot/(?P<pk>\d+)/$', LotDetailView.as_view(), name='lot_detail'),
)
