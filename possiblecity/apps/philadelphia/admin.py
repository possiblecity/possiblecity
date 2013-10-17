# philadelphia/admin.py

from django.contrib import admin

from .models import LotProfile, Neighborhood

class LotProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'address', 'neighborhood', 'basereg', 'tencode', 'brt_id')
        search_fields = ['lot__address', 'basereg', 'tencode', 'brt_id']
        list_filter = ('neighborhood',)
        raw_id_fields = ('lot',)

admin.site.register(LotProfile, LotProfileAdmin)
admin.site.register(Neighborhood)
