# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # homepage
    url(r'^$', TemplateView.as_view(template_name='homepage.html'),name='home'),

    # people
    url(r'^account/', include('account.urls')),

    #projects
    url(r'^float/', include('possiblecity.float.urls.share')),
    url(r'^explore/', include('possiblecity.float.urls.explore')),

    #places

    # blog

    # search

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
