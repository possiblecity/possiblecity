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

    url(r"^$", TemplateView.as_view(template_name="homepage.html"),name="home"),



    url(r"^admin/", include(admin.site.urls)),


    url(r"^account/social/", login_required(TemplateView.as_view(template_name="account/social.html")),
        name="social_settings"),
    url(r"^social/", include('social_auth.urls')),
    url(r"^account/", include("account.urls")),


    # blog
    #(r'^blog/', include('blog.urls')),


    # search
    #(r'^search/', include('haystack.urls')),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)