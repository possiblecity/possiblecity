# ideas/urls/explore.py

from django.conf.urls.defaults import *

from ..views.explore import IdeaDetailView, IdeaListView, IdeaListWithinFeature

urlpatterns = patterns('',
    url(r'^$', IdeaListView.as_view(), name='ideas_idea_list'),
    url(r'^(?P<app>[-\w]+)/(?P<model>[-\w]+)/(?P<slug>[-\w]+)/$', IdeaListWithinFeature.as_view(), name='ideas_idea_list_within_feature'),
    url(r'^idea/(?P<slug>[-\w]+)/$', IdeaDetailView.as_view(), name = 'ideas_idea_detail'),
)