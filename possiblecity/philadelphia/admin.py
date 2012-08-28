from django.contrib.gis import admin
from possiblecity.philadelphia.models import Lot, Parcel

class LotAdmin(admin.GeoModelAdmin):
    list_display = ('address', 'is_public', 'is_vacant', 'is_visible')

admin.site.register(Lot, LotAdmin)
admin.site.register(Parcel, admin.GeoModelAdmin)
