import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from possiblecity.uploads.models import File


@csrf_exempt
@require_POST
@login_required
def upload_photos(request):
    images = []
    for f in request.FILES.getlist("file"):
        obj = File.objects.create(upload=f, is_image=True)
        images.append({"filelink": obj.upload.url})
    return HttpResponse(json.dumps(images), mimetype="application/json")


@login_required
def recent_photos(request):
    images = [
        {"thumb": obj.upload.url, "image": obj.upload.url}
        for obj in File.objects.filter(is_image=True).order_by("-date_created")[:20]
    ]
    return HttpResponse(json.dumps(images), mimetype="application/json")
