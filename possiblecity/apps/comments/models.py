import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from actstream import action

from .signals import commented

class Comment(models.Model):
    """
    Open-ended user input.
    """

    VIA_WEB = 1
    VIA_TEXT = 2
    VIA_TWITTER = 3
    VIA_INSTAGRAM = 4
    VIA_EMAIL = 5
    VIA_CHOICES = (
        (VIA_WEB, 'Web'),
        (VIA_TEXT, 'Text'),
        (VIA_TWITTER, 'Twitter'),
        (VIA_INSTAGRAM, 'Instagram'),
        (VIA_EMAIL, 'Email'),
    )
    
    # content
    text = models.TextField()
    image = models.ImageField(blank=True, upload_to='images/comments')

    # meta
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    via = models.IntegerField(choices=VIA_CHOICES, default=VIA_WEB)
    is_public = models.BooleanField(default=True)

    # auto-generated fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # generic relations
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return u'%s' % self.text[:50]


def comment_action(sender, comment=None, target=None, **kwargs):
    action.send(comment.user, verb=u'commented', action_object=comment, 
            target=comment.content_object)

commented.connect(comment_action)
