# philadelphia/admin.py

from django.contrib import admin

from .models import LotProfile, Neighborhood

class LotProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'address', 'neighborhood', 'basereg', 'opa_code')
        search_fields = ['lot__address', 'basereg', 'opa_code']
        list_filter = ('neighborhood',)

admin.site.register(LotProfile, LotProfileAdmin)
admin.site.register(Neighborhood)
