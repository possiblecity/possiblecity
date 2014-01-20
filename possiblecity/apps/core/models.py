# core/models.py
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

object_liked.connect(liked_action)