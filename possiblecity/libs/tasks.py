from django.contrib.auth.models import User

from celery.task import Task
from social_auth.models import UserSocialAuth

from apps.friends.models import Suggestion
from .social import Provider


class ProcessSocialNetwork(Task):
    
    def run(self, user_pk, provider):
        user = User.objects.get(pk=user_pk)
        social = Provider(user, provider)
        total = 0
        for friend in social.friends():
            social_auth = UserSocialAuth.get_social_auth(
                provider=provider,
                uid=friend["id"]
            )
            if social_auth is not None:
                Suggestion.objects.create_suggestions(user, social_auth.user)
            total += 1
        return total