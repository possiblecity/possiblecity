from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="about/about.html"), name="about"),
    url(r"^what_next/$", TemplateView.as_view(template_name="about/what_next.html"), name="what_next"),
)
