from django import template

register = template.Library()

@register.filter
#capitalise the first letter of each sentence in a string
def capsentence(value):
    value = value.lower()
    return " ".join([sentence.capitalize() for sentence in value.split(" ")])