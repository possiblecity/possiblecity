# profiles/urls.py

from django.conf.urls.defaults import patterns, url

from possiblecity.profiles.views import ProfileListView, ProfileDetailView, ProfileCreateView, ProfileUpdateView

urlpatterns = patterns('',
    url(r'^create/$', ProfileCreateView.as_view(), name='profiles_profile_create'),
    url(r'^update/$', ProfileUpdateView.as_view(), name='profiles_profile_update'),
    url(r'^profile/(?P<username>\w+)/$', ProfileDetailView.as_view(),name='profiles_profile_detail'),
    url(r'^$', ProfileListView.as_view(), name='profiles_profile_list'),)
