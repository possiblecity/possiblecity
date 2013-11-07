from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink

class Profile(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    about = models.CharField(max_length=140, blank=True)
    photo = models.ImageField(upload_to='images/profiles', blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True)
    website = models.URLField(blank=True)
    twitter = models.CharField(max_length=100, blank=True)

    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ('-id',)    


    @property
    def full_name(self):
        if self.user.first_name:
            return u'%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username
        
    def __unicode__(self):
        if self.user.first_name:
            return u'%s' % self.full_name
        else:
            return u'%s' % self.user.username

    @permalink
    def get_absolute_url(self):
        return ("profiles_profile_detail", (), {"username": self.user.username} )
