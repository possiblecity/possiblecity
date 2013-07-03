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

    # about
    url(r'^about/$', RedirectView.as_view(url='/blog/2012/oct/10/introducing-possible-city/'),
        name='about'),    

    # people
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', include('possiblecity.profiles.urls.manage')),

    url(r'^people/', include('possiblecity.profiles.urls.display')),    

    #projects
    url(r'^float/share/', include('possiblecity.projects.urls.share')),
    url(r'^float/explore/', include('possiblecity.projects.urls.explore')),

    # places
    #url(r'^lotxlot/', include('possiblecity.philadelphia.urls')),


    # search
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
