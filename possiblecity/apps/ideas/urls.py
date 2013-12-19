# ideas/urls.py

from django.conf.urls import *
from django.views.generic import TemplateView

from .views.explore import IdeaDetailView, IdeaListView, IdeaListFeaturedView
from .views.share import IdeaCreateView, IdeaUpdateView

urlpatterns = patterns('',
    # user input of ideas
    url(r'^create/$',
        IdeaCreateView.as_view(),
        name='ideas_idea_create'),
    url(r'^update/(?P<pk>[\w-]+)$',
        IdeaUpdateView.as_view(),
        name='ideas_idea_update'),

    url(r'^$', IdeaListView.as_view(), name='ideas_idea_list'),
    url(r'^(?P<slug>[-\w]+)/$', IdeaDetailView.as_view(), name = 'ideas_idea_detail'),

)
