from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    
    user = models.OneToOneField(User, related_name="profile")
    about = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True, verify_exists=False)
    image = models.ImageField(upload_to='profiles', blank=True, null=True)
    is_public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username

@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    """
    Create a Profile instance for all newly created User instances.
    Run only on user creation to avoid having to check for existence
    on each call to User.save
    """
    user, created = kwargs["instance"], kwargs["created"]
    if created:
        Profile.objects.create(user=user)
