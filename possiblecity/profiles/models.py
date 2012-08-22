from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    
    user = models.OneToOneField(User, related_name="profile")
    about = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles', blank=True, null=True)
    is_public = models.BooleanField(default=True)

    @property
    def full_name(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
        
    def __unicode__(self):
        if self.user.first_name:
            return u'%s' % self.full_name
        else:
            return u'%s' % self.user.username

    def get_absolute_url(self):
        kwargs = {"username": self.user.username}
        return reverse("profiles_profile_detail", kwargs=kwargs)

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
