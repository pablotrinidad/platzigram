"""Posts model."""

# Django
from django.contrib import admin

# Models
from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin."""

    list_display = ('id', 'user', 'title', 'photo')
    search_fields = ('title', 'user__username', 'user__email')
    list_filter = ('created', 'modified')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin model."""

    list_display = ('pk', 'user', "profile")
