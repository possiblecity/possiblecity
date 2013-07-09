# profiles/urls/manage.py

from django.conf.urls.defaults import patterns, url

from ..views import ProfileCreateView, ProfileUpdateView, ProfileLoginView

urlpatterns = patterns('',
    url(r'^$', ProfileLoginView.as_view(), 
        name='profiles_profile_login'),
    url(r'^create/$', ProfileCreateView.as_view(), 
        name='profiles_profile_create'),
    url(r'^update/$', ProfileUpdateView.as_view(), 
        name='profiles_profile_update')
)
