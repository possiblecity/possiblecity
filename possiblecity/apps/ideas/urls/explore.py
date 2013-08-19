# ideas/urls/explore.py

from django.conf.urls.defaults import *

from ..views.explore import IdeaDetailView, IdeaListView

urlpatterns = patterns('',
    url(r'^$', IdeaListView.as_view(), name='ideas_idea_list'),
    url(r'^idea/(?P<slug>[-\w]+)/$', IdeaDetailView.as_view(), name = 'ideas_idea_detail'),
)