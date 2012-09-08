# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView

from possiblecity.philadelphia.api import LotResource

from django.contrib import admin
admin.autodiscover()


lot_resource = LotResource()

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # homepage
    url(r'^$', TemplateView.as_view(template_name='homepage.html'),name='home'),

    # people
    url(r'^account/', include('account.urls')),
    url(r'^profiles/', include('possiblecity.profiles.urls')),    

    #projects
    url(r'^float/', include('possiblecity.float.urls.share')),
    url(r'^ground/', include('possiblecity.float.urls.explore')),

    # network
    url(r"^connect/", include("phileo.urls")),
    
    # places
    url(r'^lotxlot/', include('possiblecity.philadelphia.urls')),

    # blog

    # search

    # api
    (r'^api/', include(lot_resource.urls)),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
