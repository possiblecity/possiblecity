from django import template
from django.utils.timesince import timesince

register = template.Library()

@register.filter
#capitalise the first letter of each sentence in a string
def capsentence(value):
    value = value.lower()
    return " ".join([sentence.capitalize() for sentence in value.split(" ")])

@register.filter(name='ago')
def ago(date):
    ago = timesince(date)
    # selects only the first part of the returned string
    return ago.split(",")[0] + " ago"