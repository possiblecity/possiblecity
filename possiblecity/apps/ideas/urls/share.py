# ideas/urls/share.py

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from ..views.share import IdeaCreateView, IdeaUpdateView

urlpatterns = patterns('',

    # float index
    url(r'^$', TemplateView.as_view(template_name='ideas/index.html'), name='ideas_index'),

    # user input of ideas
    url(r'^idea/add/$', 
        IdeaCreateView.as_view(), 
        name='ideas_idea_create'),
    url(r'^idea/update/(?P<idea_id>\d+)/$', 
        IdeaUpdateView.as_view(), 
        name='ideas_idea_update'),

)
