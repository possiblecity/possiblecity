from django.contrib.gis import admin
from possiblecity.philadelphia.models import Lot, LandUnit

admin.site.register(Lot, admin.GeoModelAdmin)
admin.site.register(LandUnit, admin.GeoModelAdmin)