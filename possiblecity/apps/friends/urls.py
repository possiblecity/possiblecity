from django.conf.urls import patterns, url

from .views import (
    friends,
    suggestions,
    ajax_request_suggestion,
    ajax_ignore_suggestion,
    ajax_accept_request,
    ajax_decline_request
)


urlpatterns = patterns(
    "",
    url(r"^$", friends, name="friends_friends"),
    url(r"^suggestions/$", suggestions, name="friends_suggestions"),
    
    url(r"^ajax/suggestions/(?P<pk>\d+)/request/$", ajax_request_suggestion, name="ajax_request_suggestion"),
    url(r"^ajax/suggestions/(?P<pk>\d+)/ignore/$", ajax_ignore_suggestion, name="ajax_ignore_suggestion"),
    url(r"^ajax/requests/(?P<pk>\d+)/accept/$", ajax_accept_request, name="ajax_accept_request"),
    url(r"^ajax/requests/(?P<pk>\d+)/decline/$", ajax_decline_request, name="ajax_decline_request"),
)
