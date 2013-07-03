# float/urls/explore.py

from django.conf.urls.defaults import *

from ..views.explore import ProjectDetailView, ProjectListView

urlpatterns = patterns('',
    url(r'^$', ProjectListView.as_view(), name='projects_project_list'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(), name = 'projects_project_detail'),
)
