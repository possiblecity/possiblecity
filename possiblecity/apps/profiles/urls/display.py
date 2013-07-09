# profiles/urls/display.py

from django.conf.urls.defaults import patterns, url

from ..views import ProfileDetailView, ProfileListView

urlpatterns = patterns('',
    url(r'^$', ProfileListView.as_view(), name='profiles_profile_list'),
    url(r'^(?P<username>[\w\.]+)/$', ProfileDetailView.as_view(), name='profiles_profile_detail'),
)
