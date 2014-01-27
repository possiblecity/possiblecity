# blog/urls.py

from django.conf.urls import include, patterns, url
from django.views.generic import YearArchiveView, MonthArchiveView,\
    WeekArchiveView, DayArchiveView, TodayArchiveView,\
    DetailView, ListView, ArchiveIndexView

from .models import Entry
from .views import *

urlpatterns = patterns('',
    url(r'^$',
        ArchiveIndexView.as_view(
            queryset=Entry.objects.live(),
            date_field="published",
            context_object_name = "entry_list"),
        name = 'text_entry_index'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/update/$',
        EntryUpdateView.as_view(),
        name = 'text_entry_update'),

    url(r'^create/$',
        EntryCreateView.as_view(),
        name = 'text_entry_create'),


    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        EntryDetailView.as_view(),
        name = 'text_entry_detail'),


    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='text_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='text_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(
            queryset=Entry.objects.live(),
            date_field="published"),
        name='text_archive_year'
    ),
    url(r"^ajax/images/(?P<entry_id>\d+)/$",
        related_images,
        name="text_related_images"
    ),
    url(r"^ajax/images/upload/$", upload_images, name="text_upload_images"),
    url(r"^ajax/images/recent/$", recent_images, name="text_recent_images")

)
