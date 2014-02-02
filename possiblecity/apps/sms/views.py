# sms/views.py
import re

import simplejson as json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


from actstream.actions import follow
from twilio.rest import TwilioRestClient

from apps.lotxlot.models import Lot
from apps.comments.models import Comment
from apps.ideas.models import Idea
from apps.profiles.models import Profile
from libs.utils import extract_hashtags, get_or_none, phone_format


@csrf_exempt
def process_sms(request):
    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET 

    phone = phone_format(re.sub('\+1','',params['From']))

    message = params['Body']
    hashtags = extract_hashtags(message)

    for tag in hashtags:
    	try:
            lookup = int(tag.replace("#", ""))
            target = get_or_none(Lot, pk=lookup)
        except ValueError:
            lookup = tag.replace("#", "")
            target = get_or_none(Idea, hashtag__icontains=lookup)

        if target:
            try:
                user = User.objects.get(profile__phone=phone)
                new_user = False
                password = None
            except User.DoesNotExist:
                user = User(username=phone)
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                profile = Profile.objects.get(user=user)
                profile.phone = phone
                profile.save()
                new_user = True

            comment = Comment(user=user, 
                              via=Comment.VIA_TEXT, 
                              text=message,
	    		              content_type=ContentType.objects.get_for_model(target), 
                              object_id=target.id)
            follow(user, target, actor_only=False)

            comment.save()

            status = "OK"

            break

        else:
            user = None
            new_user = False
            password = None
            status = "ERROR"

    context = {
        "target": target,
        "user": user,
        "new_user": new_user,
        "password": password
    }

    reply = render_to_string("sms/reply.txt", context)


    TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', None)

    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    sms = client.messages.create(
                to=phone,
                from_=TWILIO_FROM_NUMBER,
                body=reply
            )

    if new_user:
        new_user_msg = render_to_string("sms/new_user.txt", context)

        sms = client.messages.create(
                to=phone,
                from_=TWILIO_FROM_NUMBER,
                body=new_user_msg
            )


    return HttpResponse(json.dumps({
                "status": status,
                }
            ), mimetype="application/json")


