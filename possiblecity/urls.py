# urls.py

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # admin
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),

    # about
    #url(r'^about/$', RedirectView.as_view(url='/blog/2012/oct/10/introducing-possible-city/'),name='about'),
    
    # blog
    #url(r'^blog/', include('apps.text.urls')),

    # people
    #url(r"^friends/", include("apps.friends.urls")),
    #url(
    #    r"^account/social/connections/$",
    #    TemplateView.as_view(template_name="account/connections.html"),
    #    name="account_social_connections"
    #),
    #url(r"^account/social/", include("social_auth.urls")),

    url(r"^account/", include("account.urls")),   
    url(r"^profiles/", include("apps.profiles.urls")),   

    #ideas
    url(r'^ideas/float/', include('apps.ideas.urls.share')),
    url(r'^ideas/explore/', include('apps.ideas.urls.explore')),

    # places
    #url(r'^lotxlot/', include('possiblecity.philadelphia.urls')),


    # search
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

