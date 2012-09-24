# text/views.py

from django.conf import settings
from django.db.models import F
from django.views.generic import DateDetailView, ArchiveIndexView

from possiblecity.text.models import Entry

class EntryDetailView(DateDetailView):
    queryset = Entry.objects.live()
    context_object_name = "entry"
    date_field="published"

