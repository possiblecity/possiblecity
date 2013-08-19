from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.models import User

from social_auth.models import UserSocialAuth

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