# float/models.py

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.html import strip_tags

#from taggit.managers import TaggableManager

from possiblecity.float.fields import PositionField
from possiblecity.float.managers import ProjectManager

class Idea(models.Model):
	"""
		Defines an idea- a concept for an intervention in a city that is less 
		fully formed than a project; usually just a sentence or two expressing
		a desire or a need. Not sure yet if we will implement this on the site.
		Just a placeholder for now.
	"""
	description = models.CharField(max_length=140)
	agent = models.ForeignKey(User, help_text="The person submitting the idea")

class Project(models.Model):
    """
       Defines a project, which consists of ideas, plans, images, and drawings for 
       an urban intervention. Users upload projects which can then be networked with
       other users, other projects, or locations within the city.
    """

    STATUS_PENDING = 1
    STATUS_PUBLISHED = 2
    STATUS_REJECTED = 3
    STATUS_HIDDEN = 4
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_HIDDEN, 'Hidden'),
    )

    # Project owner manages these fields
    title = models.CharField(max_length=250)
    tagline = models.CharField(max_length=500, help_text="A sentence summary of the project.")
    description = models.TextField()


    # Categorization
    #tags = TaggableManager(blank=True)

    # Site admin manages these fields
    agent = models.ForeignKey(User, help_text="The owner of the project.")
    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING,
                                 help_text="Only projects with published status will be publicly displayed.")
    enable_comments = models.BooleanField(default=True)
    moderate_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    grounded = models.DateField("Date Grounded", blank=True, null=True)

    # autogenerated fields
    description_html = models.TextField(blank=True,editable=False)
    created = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)
    floated = models.DateField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.floated:
             if self.status == self.STATUS_PUBLISHED:
                self.floated = datetime.datetime.now()

        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.title)
       
    @permalink
    def get_absolute_url(self):
        return ('float_project_detail', [str(self.slug)])    

class ProjectImage(models.Model):
    """
        An image used to help describe a project.
    """
    image = models.ImageField(upload_to='images/project/')
    title = models.CharField(max_length=255)
    caption = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True, help_text="This file is publicly available.")

    project = models.ForeignKey(Project)
    agent = models.ForeignKey(User)

    # autogenerated fields
    added = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)

    def __unicode__(self):
        return u'%s' % self.title
