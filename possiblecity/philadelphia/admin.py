from django.contrib.gis import admin
from philadelphia.models import PhlParcel, PhlLand, PhlPublicVacantLot

admin.site.register(PhlParcel, admin.GeoModelAdmin)
admin.site.register(PhlPublicVacantLot, admin.GeoModelAdmin)