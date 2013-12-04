from django.contrib import admin

from .models import Idea, IdeaVisual, IdeaFile


class VisualInline(admin.TabularInline):
    model = IdeaVisual

class FileInline(admin.TabularInline):
    model = IdeaFile

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('tagline', 'user', 'via', 'featured')
    list_editable = ('via', 'featured')
    search_fields = ['tagline',]
    raw_id_fields = ('lots',)
 
    inlines = [ VisualInline, ]


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaVisual)
admin.site.register(IdeaFile)
