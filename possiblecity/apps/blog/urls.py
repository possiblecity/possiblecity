# blog/urls.py

from django.conf.urls.defaults import include, patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView,\
    WeekArchiveView, DayArchiveView, TodayArchiveView,\
    DetailView, ListView

from blog.models import Post
from blog.views import PostIndexView, PostDetailView

urlpatterns = patterns('',
    url(r'^$', PostIndexView.as_view(), name = 'blog_post_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name = 'blog_post_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(
            queryset=Post.objects.live(),
            date_field="date_published"),
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(
            queryset=Post.objects.live(),
            date_field="date_published"),
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset=Post.objects.live(),
            date_field="date_published"),
        name='blog_archive_year'
    ),
)
