# blog/admin.py

from django.contrib import admin

from blog.models import Entry, EntryImage, InlineImage

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryImage)
admin.site.register(InlineImage)