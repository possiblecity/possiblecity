import datetime

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.utils.safestring import mark_safe

from django_markup.fields import MarkupField
from django_markup.markup import formatter
from taggit.managers import TaggableManager

from text.models import EntryBase
from images.models import RelatedImageBase


class Entry(EntryBase):
    """
        A blog entry. Inherits basic fields from text.models.EntryBase.
        Adds tags, markup, commenting, images
    """
    tags = TaggableManager(blank=True)
    enable_comments = models.BooleanField(default=True)
    markup = MarkupField(default=settings.BLOG_MARKUP_DEFAULT)

    # Fields to store generated HTML. For use with a markup syntax such as Markdown or Textile
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # autocreated fields
    visits = models.IntegerField(default=0, editable=False) #to keep track of most popular posts

    @permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', None, {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.day,
            'slug': self.slug
        })

    def render_markup(self):
        if settings.BLOG_MARKUP_DEFAULT == 'wysiwyg':
            self.markup = "none"
            self.body_html = self.body
            self.excerpt_html = self.excerpt
        else:
            self.body_html = mark_safe(formatter(self.body, filter_name=self.markup))
            self.excerpt_html = mark_safe(formatter(self.excerpt, filter_name=self.markup))

    def get_main_image(self):
        pass


    def save(self, force_insert=False, force_update=False):
        self.render_markup()
        super(Post, self).save(force_insert, force_update)

class EntryImage(RelatedImageBase):
    """
        An orderable image attached to a blog entry.
        Inherits basic fields and behavior from images.models.RelatedImageBase
    """
    image = models.ImageField(upload_to='images/entries/')
    entry = models.ForeignKey(Entry)
