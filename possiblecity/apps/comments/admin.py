from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):  
    list_display = ["user", "content_type", "created", "is_public"]
    list_filter = ["is_public", "content_type"]


admin.site.register(Comment, CommentAdmin)
