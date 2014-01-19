# lotxlot_tags.py
from urllib import urlencode

from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag()
def google_image_url(lot, width, height, fov='105'):
	url = "http://maps.googleapis.com/maps/api/streetview"
	params = {
		"size": "%sx%s" % (width, height),
		"location": "%f,%f" % (lot.coord.y, lot.coord.x),
		"sensor": "false",
		"fov": fov,
		"key": settings.GOOGLE_MAPS_API_KEY,
	}
	return url + "?" + urlencode(params)