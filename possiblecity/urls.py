# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView


from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # about
    url(r'^about/$', RedirectView.as_view(url='/blog/2012/oct/10/introducing-possible-city/'),
        name='about'),
    
    # blog
    url(r'^blog/', include('possiblecity.text.urls')),

    # homepage
    url(r'^$', RedirectView.as_view(url='/blog'),name='home'),

    # people
    #url(r'^account/', include('account.urls')),
    url(r'^profiles/', include('possiblecity.profiles.urls')),    

    #projects
    #url(r'^float/', include('possiblecity.float.urls.share')),
    #url(r'^ground/', include('possiblecity.float.urls.explore')),

    # network
    #url(r"^connect/", include("phileo.urls")),
    
    # places
    #url(r'^lotxlot/', include('possiblecity.philadelphia.urls')),


    # search

    # api
    #(r'^api/', include(lot_resource.urls)),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
