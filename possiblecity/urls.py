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
    
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),

    # about
    url(r'^about/$', RedirectView.as_view(url='/blog/2012/oct/10/introducing-possible-city/'),
        name='about'),
    
    # blog
    url(r'^blog/', include('apps.text.urls')),

    # homepage
    url(r'^$', RedirectView.as_view(url='/blog'),name='home'),

    # about
    url(r'^about/$', RedirectView.as_view(url='/blog/2012/oct/10/introducing-possible-city/'),
        name='about'),    

    # people
    url(r"^friends/", include("apps.friends.urls")),
    url(
        r"^account/social/connections/$",
        TemplateView.as_view(template_name="account/connections.html"),
        name="account_social_connections"
    ),
    url(r"^account/social/", include("social_auth.urls")),
    url(
        r"^account/login/$",
        TemplateView.as_view(template_name="account/signup.html"),
        name="account_login"
    ),
    url(
        r"^account/signup/$",
        TemplateView.as_view(template_name="account/signup.html"),
        name="account_signup"
    ),
    url(r"^account/", include("account.urls")),    

    #projects
    url(r'^projects/float/', include('apps.projects.urls.share')),
    url(r'^projects/explore/', include('apps.projects.urls.explore')),

    # places
    #url(r'^lotxlot/', include('possiblecity.philadelphia.urls')),


    # search
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
