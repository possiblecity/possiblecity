# text/admin.py

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Entry, EntryImage

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryImage)
