# text/admin.py

from django.contrib import admin

from text.models import Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Entry, EntryAdmin)
