# philadelphia/admin.py

from django.contrib import admin

from .models import LotProfile, Neighborhood

class LotProfileAdmin(admin.ModelAdmin):
	list_display = ('address', 'neighborhood', 'basereg', 'opa_code')

admin.site.register(LotProfile, LotProfileAdmin)
admin.site.register(Neighborhood)