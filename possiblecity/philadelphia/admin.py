from django.contrib.gis import admin
from django.db.models import Count

from possiblecity.philadelphia.models import Lot, Parcel

class LotAdmin(admin.GeoModelAdmin):
    list_display = ('address', 'is_public', 'is_vacant', 'is_visible')
    raw_id_fields = ('parcel',)
    list_filter = ('is_vacant', 'is_available', 
        'is_visible', 'has_vacancy_violation', 'has_vacancy_license',
        'has_vacant_building')
    search_fields = ['address']

class ParcelAdmin(admin.GeoModelAdmin):
    list_display = ('objectid', 'mapreg',)
    search_fields =['objectid',]

admin.site.register(Lot, LotAdmin)
admin.site.register(Parcel, ParcelAdmin)
