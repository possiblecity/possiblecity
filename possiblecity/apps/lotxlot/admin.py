# lotxlot/admin.py

from django.contrib import admin

from .models import Lot

class LotAdmin(admin.ModelAdmin):
	list_display = ('id', 'address', 'city', 'state', 'is_vacant', 'is_public', 'is_visible',)
	list_editable = ('is_visible',)
	search_fields = ['address',]
	list_filter = ('city',)

admin.site.register(Lot, LotAdmin)
