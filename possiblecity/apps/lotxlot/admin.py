# lotxlot/admin.py

from django.contrib import admin

from apps.ideas.models import Idea

from .models import Lot

class IdeaInline(admin.TabularInline):
    model = Idea

class LotAdmin(admin.ModelAdmin):
	list_display = ('id', 'address', 'city', 'state', 'is_vacant', 'is_public', 'is_visible',)
	list_editable = ('is_visible',)
	search_fields = ['address',]
	list_filter = ('city',)
        
        inlines = [ IdeaInline, ]

admin.site.register(Lot, LotAdmin)
