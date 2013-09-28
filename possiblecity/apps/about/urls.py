from django.conf.urls.defaults import *

from .views import AboutView


urlpatterns = patterns('',
    url(r"^$", AboutView.as_view(), name="about"),
)
