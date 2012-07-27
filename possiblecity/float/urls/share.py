# float/urls/share.py

from django.conf.urls.defaults import *

from possiblecity.float.views.share import ProjectCreateView, ProjectUpdateView

urlpatterns = patterns('',

    # share index
    url(r'^$', 'share_index', name="share"),

    # user input of ideas
    url(r'^project/add/$', ProjectCreateView.as_view(), name='float_project_create'),
    url(r'^project/edit/(?P<idea_id>\d+)/$', ProjectUpdateView.as_view(), name='float_project_update'),

)
