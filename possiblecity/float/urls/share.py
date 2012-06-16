# float/urls/share.py

from django.conf.urls.defaults import *

from float.models import *

urlpatterns = patterns('',
    url(r'^projects/$', ProjectListView.as_view(), name='float_project_list'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(), name = 'float_project_detail'),
)

urlpatterns = patterns('actionmanual.portfolio.views.share',

    # share index
    url(r'^$', 'share_index', name="share"),

    # user input of ideas
    url(r'^project/add/$', ProjectCreateView.asView(), name='float_project_create'),
    url(r'^project/edit/(?P<idea_id>\d+)/$', ProjectUpdateView.asView(), name='float_project_update'),

)
