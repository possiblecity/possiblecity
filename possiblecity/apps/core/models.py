# core/models.py
from django.db.models.signals import post_save

from actstream.models import Follow
from actstream import action
from phileo.signals import object_liked, object_unliked
from notification import models as notification

def liked_action(sender, request, object=None, like=None, target=None, **kwargs):
    action.send(request.user, verb=u'favorited', target=like.receiver)
    if hasattr(like.receiver, 'user'):
       notification.send([like.receiver.user, ], "new_favorite", 
           { "target": like.receiver, "sender": like.sender })

def unliked_action(sender, request, object=None, target=None, **kwargs):
    action.send(request.user, verb=u'unfavorited', target=object)

def notify_following(sender, instance, **kwargs):
    follower = instance.user
    target = instance.follow_object
    if hasattr(target, 'user'):
        notify_list = [ target.user,]
    elif hasattr(target, 'first_name'):
        notify_list = [ target, ]
    else:
        return
    notification.send( notify_list, "new_follower", 
        { "follower": follower, "target": target })	

object_liked.connect(liked_action)

post_save.connect(notify_following, sender=Follow, dispatch_uid="notify_following")
