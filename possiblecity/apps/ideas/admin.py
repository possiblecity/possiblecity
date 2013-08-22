from django.contrib import admin

from .models import Idea, IdeaVisual

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('tagline', 'lot', 'user', 'via')
    list_editable = ('via',)
    search_fields = ['tagline',]
    raw_id_fields = ('lot',)




admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaVisual)
