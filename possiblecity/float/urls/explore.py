# float/urls/explore.py

from django.conf.urls.defaults import *

from float.views import ProjectDetailView, ProjectListView

urlpatterns = patterns('',
    url(r'^projects/$', ProjectListView.as_view(), name='float_project_list'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(), name = 'float_project_detail'),
)