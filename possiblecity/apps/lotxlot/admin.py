# lotxlot/admin.py

from django.contrib import admin

from apps.ideas.models import Idea

from .models import Lot, Comment

class IdeaInline(admin.TabularInline):
    model = Idea.lots.through
    extra = 1
    verbose_name = "ideas"

class LotAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'get_neighborhood', 'city', 'state', 'is_vacant', 'is_public', 'is_visible', 'updated')
    list_editable = ('is_vacant', 'is_visible',)
    search_fields = ['address',]
    list_filter = ('is_vacant', 'is_public', 'city', 'profile__neighborhood')
        
    inlines = [ IdeaInline, ]

    def get_neighborhood(self, obj):
        return '%s'%(obj.profile.neighborhood)
    get_neighborhood.short_description = 'Neighborhood'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'lot', 'user', 'via', 'updated')
    list_editable = ('via',)
    search_fields = ['user', 'text']
    list_filter = ('via',)
    raw_id_fields = ('lot', 'user' )    

admin.site.register(Lot, LotAdmin)
admin.site.register(Comment, CommentAdmin)
