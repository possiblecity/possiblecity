# blog/views.py

import json

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DateDetailView, ArchiveIndexView, UpdateView, CreateView

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from braces.views import SuperuserRequiredMixin
from .models import Entry, EntryImage
from .forms import EntryForm

class EntryDetailView(DateDetailView):
    queryset = Entry.objects.live()
    context_object_name = "entry"
    date_field = "published"

class EntryUpdateView(SuperuserRequiredMixin, UpdateView):
    model=Entry

class EntryCreateView(SuperuserRequiredMixin, CreateView):
    model = Entry
    #form_class = EntryForm


@login_required
def related_images(request,entry_id):
    images = [
        {"thumb": obj.original.url, "image": obj.original.url}
        for obj in EntryImage.objects.filter(entry__id=entry_id)
    ]
    return HttpResponse(json.dumps(images), mimetype='application/json')


@csrf_exempt
@require_POST
@login_required
def upload_images(request):
    images = []
    for f in request.FILES.getlist("file"):
        obj = EntryImage.objects.create(original=f)
        images.append({"filelink": obj.original.url})
    return HttpResponse(json.dumps(images), mimetype="application/json")


@login_required
def recent_images(request):
    images = [
        {"thumb": obj.original.url, "image": obj.original.url}
        for obj in EntryImage.objects.all().order_by("-created")[:20]
    ]
    return HttpResponse(json.dumps(images), mimetype="application/json")
