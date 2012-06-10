from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase


class Profile(ProfileBase):
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)
    image = models.ImageField(_("image"), upload_to='profiles')


from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends import google
from social_auth.signals import socialauth_registered

def get_social_extras(sender, user, response, details, **kwargs):
    """
        A signal that will grab a photo from a social networking site
        and add that photo to the Profile model when a user registers via
        that social network
    """

    user.is_new = True
    if user.is_new:

        if "id" in response:

            from urllib2 import urlopen, HTTPError
            from django.template.defaultfilters import slugify
            from django.core.files.base import ContentFile

            try:
                url = None
                if sender == FacebookBackend:
                    url = "http://graph.facebook.com/%s/picture?type=large"\
                    % response["id"]
                elif sender == google.GoogleOAuth2Backend and "picture" in response:
                    url = response["picture"]

                elif sender == TwitterBackend:
                    url = response["profile_image_url"]

                if url:
                    social_image = urlopen(url)
                    profile = Profile(user=user)

                    profile.image.save(slugify(user.username + " social") + '.jpg',
                        ContentFile(social_image.read()))

                    profile.save()

            except HTTPError:
                pass

    return False

socialauth_registered.connect(get_social_extras, sender=None)
