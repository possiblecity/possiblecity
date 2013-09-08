from django import template
from django.db.models import get_model
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
     
class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
 
def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

class LatestFeaturedContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))
    
    def render(self, context):
        context[self.varname] = self.model._default_manager.filter(featured=True)[:self.num]
        return ''
 
def get_latest_featured(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestFeaturedContentNode(bits[1], bits[2], bits[4])
    
get_latest = register.tag(get_latest)
get_latest_featured = register.tag(get_latest_featured)