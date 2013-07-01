# profiles/urls/manage.py

from django.conf.urls.defaults import patterns, url

from ..views import ProfileCreateView, ProfileUpdateView

urlpatterns = patterns('',
    url(r'^create/$', ProfileCreateView.as_view(), name='profile_create'),
    url(r'^update/$', ProfileUpdateView.as_view(), name='profile_update')
)
