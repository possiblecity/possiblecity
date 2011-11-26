# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # homepage
    #url(r'^$', 'possiblecity.views.index', name = 'home'),

    # blog
    (r'^blog/', include('blog.urls')),

    # about
    #url(r'^$', TemplateView.as_view(), template_name = "about.html", name = 'about'),

)