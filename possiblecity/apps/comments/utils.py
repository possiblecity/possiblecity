# comments/utils.py

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from apps.ideas.models import Idea
from .models import Comment


def convert_to_comments():
	ct = ContentType.objects.get(name='lot')
	ideas = Idea.objects.all()
	for idea in ideas:
		if not idea.description:
			text = idea.tagline
			user = idea.user
			lots = idea.lots.all()
			
			for lot in lots:
				comment, created = Comment.objects.get_or_create(text=text, 
    				user=user, content_type=ct, object_id = lot.id)
    			if created:
    				comment.save()
    				print "create new comment %s" % comment.text
