# urls.py
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView

import autocomplete_light

autocomplete_light.autodiscover()
admin.autodiscover()

# api machinery
from rest_framework import routers

from apps.core.views import HomepageView
from apps.lotxlot.views import (LotApiViewSet, LotIdeaApiViewSet, LotPointApiViewSet, 
    LotCommentApiViewSet, VacantLotApiViewSet, VacantLotPointApiViewSet)
from apps.philadelphia.views import NeighborhoodApiViewSet

router = routers.DefaultRouter()
router.register(r'lots/polys', LotApiViewSet, base_name='api-lot')
router.register(r'lots/points', LotPointApiViewSet, base_name='api-lot-point')
router.register(r'lots/vacant/polys', VacantLotApiViewSet, base_name='api-vacant-lot')
router.register(r'lots/vacant/points', VacantLotPointApiViewSet, base_name='api-vacant-lot-point')
router.register(r'lots/ideas', LotIdeaApiViewSet, base_name='api-lot-idea')
router.register(r'lots/comments', LotCommentApiViewSet, base_name='api-lot-comment')
router.register(r'lots/activity', LotCommentApiViewSet, base_name='api-lot-activity')
router.register(r'philadelphia/neighborhoods', NeighborhoodApiViewSet, base_name='api-neighborhood')


urlpatterns = patterns("",
    # admin
    url(r"^admin/", include(admin.site.urls)),

    # homepage

    url(r"^$", HomepageView.as_view(), name="home"),

    # api
    url(r"^api/", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),

    # about
    url(r"^about/", include("apps.about.urls")),
    
    # blog
    #url(r'^blog/', include('apps.text.urls')),


    # social auth # people

    url(
        r"^account/social/connections/$",
        TemplateView.as_view(template_name="account/connections.html"),
        name="account_social_connections"
    ),
    url(r"^account/social/", include("social_auth.urls")),

    url(r"^account/", include("account.urls")),   
    url(r"^people/", include("apps.profiles.urls")),   

    # ideas
    url(r"^projects/", include("apps.ideas.urls")),

    # places
    url(r"^lots/", include("apps.lotxlot.urls")),
    url(r"^lotxlot/", RedirectView.as_view(url="/lots/")),

    # js urls
    url(r"^jsreverse/$", "django_js_reverse.views.urls_js", name="js_reverse"),

    url(r"^likes/", include("phileo.urls")),
    
    url(r"^comments/", include("apps.comments.urls")),

    url(r"^activity/", include("actstream.urls")),


    # autocomplete forms
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r"^notifications/", include("notification.urls")),

)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

