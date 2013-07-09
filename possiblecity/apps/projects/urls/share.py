# projects/urls/share.py

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from ..views.share import ProjectCreateView, ProjectUpdateView

urlpatterns = patterns('',

    # float index
    url(r'^$', TemplateView.as_view(template_name='projects/index.html'), name='projects_project_index'),

    # user input of ideas
    url(r'^project/add/$', 
        ProjectCreateView.as_view(), 
        name='projects_project_create'),
    url(r'^project/edit/(?P<idea_id>\d+)/$', 
        ProjectUpdateView.as_view(), 
        name='projects_project_update'),

)
