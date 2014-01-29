# sms/views.py
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from libs.utils import extract_hashtags, get_or_none, phone_format

from apps.lotxlot.models import Lot
from apps.comments.models import Comment
from apps.ideas.models import Idea
from apps.profiles.models import Profile


@csrf_exempt
def process_sms(request):
    if request.method == 'POST':
        params = request.POST
        phone = phone_format(re.sub('\+1','',params['From']))

        try:
        	user = User.objects.get(profile__phone=phone)
        except User.DoesNotExist:
        	user = User(username=phone)
        	user.save()
        	profile = Profile.objects.get(user=user)
        	profile.phone = phone
        	profile.save()

        message = params['Body']

        hashtags = extract_hashtags(message)

        for tag in hashtags:
        	try:
        		target = get_or_none(Lot, pk=int(tag.replace("#", "")))
			except ValueError:
				target = get_or_none(Idea, hashtag=tag.replace("#", "")))

			if target:
		    	Comment.objects.create(user=user, via=Comment.VIA_TEXT, 
		    		content_type=target.content_type, object_id=target.id)


