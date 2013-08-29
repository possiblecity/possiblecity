from django.contrib import admin

from .models import Idea, IdeaVisual

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('tagline', 'user', 'via')
    list_editable = ('via',)
    search_fields = ['tagline',]
    raw_id_fields = ('lots',)




admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaVisual)
