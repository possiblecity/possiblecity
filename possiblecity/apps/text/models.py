# text/models.py
import datetime

from markdown import markdown

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.safestring import mark_safe

from taggit.managers import TaggableManager

from possiblecity.text.managers import EntryManager

class TitleBase(models.Model):
    """
        An abstract content block with a title.
    """
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

class BlurbBase(models.Model):
    """
        An abstract content block with a text blurb.
    """
    text = models.TextField()

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        abstract = True

class ArticleBase(TitleBase, BlurbBase):
    """
        An abstract content block with a title, text blurb, and excerpt.
    """
    excerpt = models.TextField(blank=True, null=True)

    class Meta:
        abstract=True

class StatusMixin(models.Model):
    """
        Allow for a content to be marked with a status
    """
    STATUS_LIVE = 1
    STATUS_HIDDEN = 2
    STATUS_PENDING = 3
    STATUS_DRAFT = 4
    STATUS_CHOICES = (
        (STATUS_LIVE, 'Live'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_HIDDEN, 'Hidden'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_DRAFT,
                                              help_text="Only content with live status will be publicly displayed.")

    class Meta:
        abstract = True

        
class PostMixin(models.Model):
    """
        A mixin for a catalogued content type.
    """

    # metadata
    author = models.ForeignKey(User)
    published = models.DateTimeField(default=datetime.datetime.now)

    #auto-generated fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-published']
        get_latest_by = '-published'

    def get_previous(self):
        return self.get_previous_by_published(status=self.STATUS_LIVE)

    def get_next(self):
        return self.get_next_by_published(status=self.STATUS_LIVE)


class EntryBase(ArticleBase, StatusMixin, PostMixin):
    """
        An article with status and post information
    """

    slug = models.SlugField(unique_for_date='published')

    class Meta:
        abstract = True

class Entry(EntryBase):
    """
        A blog entry. Inherits basic fields from text.models.EntryBase.
    """
    objects = EntryManager()

    link = models.URLField(blank=True)
    
    tags = TaggableManager(blank=True)
    enable_comments = models.BooleanField(default=False)

    # Fields to store generated HTML. For use with a markup syntax such as Markdown or Textile
    excerpt_html = models.TextField(editable=False, blank=True)
    text_html = models.TextField(editable=False, blank=True)
    
    def render_markup(self):
        self.text_html = markdown(self.text)
        self.excerpt_html = markdown(self.excerpt)

    @permalink
    def get_absolute_url(self):
        return ('text_entry_detail', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.day,
            'slug': self.slug
        })

    # the following method is optional
    def get_twitter_message(self):
        return u'%s - %s'\
        % (self.title, self.excerpt)

    def save(self, *args, **kwargs):
        self.render_markup()
        super(Entry, self).save(*args, **kwargs)


class EntryImage(models.Model):
    """
    
    An image associated with a blog entry

    """
    
    file = models.ImageField(upload_to='images/blog/')
    title = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    entry = models.ForeignKey(Entry, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

