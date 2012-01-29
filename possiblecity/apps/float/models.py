# float/models.py

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.html import strip_tags

from taggit.managers import TaggableManager

from float.fields import PositionField
from float.managers import ProjectManager

class Idea(models.Model):
    pass

class Project(models.Model):
    """

       Defines a design project.

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
    website = models.URLField(blank=True)
    completed = models.DateField(blank=True, null=True)

    owner = models.ForeignKey(User, help_text="The owner of the project.")

    # Categorization.
    tags = TaggableManager(blank=True)

    # Site admin manages these fields
    slug = models.SlugField(unique=True,
                            help_text="Suggested value automatically generated from title. Must be unique.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING,
                                 help_text="Only float with published status will be publicly displayed.")
    enable_comments = models.BooleanField(default=True)
    moderate_comments = models.BooleanField(default=True)

    # autogenerated fields
    description_html = models.TextField(blank=True,editable=False)
    added = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)
    published = models.DateField(editable=False, blank=True, null=True)

    def save(self, force_insert=False, force_update=False):
        if self.status == 2:
            if not self.published:
                self.published = datetime.datetime.now()
        else:
            if self.published:
                self.published = None

        super(Project, self).save(force_insert, force_update)

    def __unicode__(self):
        return u'%s' % (self.title)


class ProjectImage(models.Model):

    image = models.ImageField(upload_to='images/project/')
    title = models.CharField(max_length=255)
    caption = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=True, help_text="This file is publicly available.")

    project = models.ForeignKey(Project)

    order = models.PositiveIntegerField(unique_for_field=project)
    is_main = models.BooleanField('Main image', default=False)

    # autogenerated fields
    added = models.DateField(auto_now_add=True, editable=False)
    modified = models.DateField(auto_now=True, editable=False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        if self.is_main:
            related_images = self.objects.filter(self, self.project)
            related_images.update(is_main=False)

        super(ProjectImage, self).save(*args, **kwargs)