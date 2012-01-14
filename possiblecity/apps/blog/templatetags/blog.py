from django import template
from django.conf import settings
from django.db import models

import re

Post = models.get_model('blog', 'post')

register = template.Library()


class LatestPosts(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        posts = Post._default_manager.live()[:self.limit]
        if posts and (self.limit == 1):
            context[self.var_name] = posts[0]
        else:
            context[self.var_name] = posts
        return ''

@register.tag
def get_latest_posts(parser, token):
    """
    Gets any number of latest posts and stores them in a variable.

    Syntax::

        {% get_latest_posts [limit] as [var_name] %}

    Example usage::

        {% get_latest_posts 10 as latest_post_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestPosts(format_string, var_name)


class PopularPosts(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        posts = Post._default_manager.live().order_by('-visits')[:self.limit]
        if posts and (self.limit == 1):
            context[self.var_name] = posts[0]
        else:
            context[self.var_name] = posts
        return ''

@register.tag
def get_popular_posts(parser, token):
    """
    Gets any number of most popular posts and stores them in a variable.

    Syntax::

        {% get_popular_posts [limit] as [var_name] %}

    Example usage::

        {% get_popular_posts 10 as popular_post_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return PopularPosts(format_string, var_name)


@register.filter
def get_links(value):
    """
     Extracts links from a ``Post`` body and returns a list.

     Template Syntax::

     {{ post.body|markdown:"safe"|get_links }}

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


class PostArchive(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        dates = Post._default_manager.live().dates('date_published', 'month', order='DESC')
        if dates:
            context[self.var_name] = dates
        return ''

@register.tag
def get_post_archive(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return PostArchive(var_name)