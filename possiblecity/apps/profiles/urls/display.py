# profiles/urls/display.py

from django.conf.urls.defaults import patterns, url

from ..views import ProfileDetailView

urlpatterns = patterns('',
    url(r'^(?P<username>[\w\.]+)/$', ProfileDetailView.as_view(), name='profiles_profile_detail'),
)
