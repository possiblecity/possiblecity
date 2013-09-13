import requests

from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from social_auth.models import UserSocialAuth

from apps.profiles.models import Profile

from .tasks import ProcessSocialNetwork


def prevent_duplicates(backend, uid, user=None, *args, **kwargs):
    details = kwargs.get("details")
    request = kwargs.get("request")
    
    if not user and "email" in details:
        user_exists = User.objects.filter(email__iexact=details["email"].strip()).exists()
        social_auths = UserSocialAuth.objects.filter(user__email__iexact=details["email"].strip())
        if user_exists and not social_auths.filter(provider=backend.name).exists():
            messages.add_message(
                request,
                messages.ERROR,
                "A user with that email address already exists."
            )
            return redirect("home")
    return None

def import_friends(backend, uid, user=None, *args, **kwargs):
    ProcessSocialNetwork.delay(user_pk=user.pk, provider=backend.name)


def get_user_avatar(backend, details, response, social_user, uid,\
                user, *args, **kwargs):

    url = None
    if getattr(backend, 'name', None) == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    elif getattr(backend, 'name', None) == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')

    if url:
        backend = getattr(backend, 'name', None)
        social_user.extra_data['photo'] = url
        social_user.save()

def update_user_profile(user, social_user, uid, backend, *args, **kwargs):
    if user.is_new:
        profile = Profile.objects.get(user=user)
        url = social_user.extra_data['photo']
        avatar = requests.get(url)
        filename = "%s_%s.jpg" % (user.username, getattr(backend, 'name', None))
        profile.photo.save(filename, ContentFile(avatar.content))
        profile.save()



        