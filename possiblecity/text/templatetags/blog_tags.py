from django import template
from django.conf import settings
from django.db import models

import re

Entry = models.get_model('blog', 'entry')

register = template.Library()


class LatestEntries(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        entries = Entry.objects.live()[:self.limit]
        if entries and (self.limit == 1):
            context[self.var_name] = entries[0]
        else:
            context[self.var_name] = entries
        return ''

@register.tag
def get_latest_entries(parser, token):
    """
    Gets any number of latest entries and stores them in a variable.

    Syntax::

        {% get_latest_entries [limit] as [var_name] %}

    Example usage::

        {% get_latest_entries 10 as latest_entry_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestEntries(format_string, var_name)


class PopularEntries(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        entries = Entry._default_manager.live().order_by('-visits')[:self.limit]
        if entries and (self.limit == 1):
            context[self.var_name] = entries[0]
        else:
            context[self.var_name] = entries
        return ''

@register.tag
def get_popular_entries(parser, token):
    """
    Gets any number of most popular entries and stores them in a variable.

    Syntax::

        {% get_popular_entries [limit] as [var_name] %}

    Example usage::

        {% get_popular_entries 10 as popular_entries_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return PopularEntries(format_string, var_name)


@register.filter
def get_links(value):
    """
     Extracts links from a ``Entry`` body and returns a list.

     Template Syntax::

     {{ entry.body|markdown:"safe"|get_links }}

     """
    try:
        from BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(value)
        return soup.findAll('a')
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in 'get_links' filter: BeautifulSoup isn't installed."
        pass
    return value

class EntryArchive(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        dates = Entry._default_manager.live().dates('published', 'month', order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''

@register.tag
def get_entry_archive(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return EntryArchive(var_name)

class EntryArchive(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        dates = Entry._default_manager.live().dates('published', 'month', order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''

@register.tag
def get_entry_archive(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return EntryArchive(var_name)