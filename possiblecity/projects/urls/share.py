# float/urls/share.py

from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from possiblecity.float.views.share import ProjectCreateView, ProjectUpdateView

urlpatterns = patterns('',

    # float index
    url(r'^$', TemplateView.as_view(template_name='float/index.html'), name='float'),

    # user input of ideas
    url(r'^project/add/$', 
        ProjectCreateView.as_view(template_name='float/create_project.html'), 
        name='float_project_create'),
    url(r'^project/edit/(?P<idea_id>\d+)/$', ProjectUpdateView.as_view(), name='float_project_update'),

)
