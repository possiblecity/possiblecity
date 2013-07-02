# text/admin.py

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse

from redactor.widgets import AdminRedactorEditor

from possiblecity.text.models import Entry, EntryImage

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
           models.TextField:{'widget': 
               AdminRedactorEditor
           }
    }

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryImage)
