# blog/admin.py

from django.contrib import admin

from possiblecity.blog.models import Entry, EntryImage

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryImage)