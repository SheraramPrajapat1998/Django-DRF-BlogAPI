from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = ('title', 'slug', 'author', 'body', 'image',
                    'status', 'publish', 'created_at', 'updated_at', )
    list_filter = ('status', 'created_at', 'updated_at',)
    raw_id_fields = ('author',)
    search_fields = ('title', 'slug', 'body')
    date_hierarchy = 'publish'
