from django.db import models

from idios.models import ProfileBase

class Profile(ProfileBase):
    name = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    website = models.URLField(null=True, blank=True, verify_exists=False)
    image = models.ImageField(upload_to='profiles')
    is_public = models.BooleanField(default=True)