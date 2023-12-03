from django.contrib import admin
from .models import Collection, Bookmark


@admin.register(Bookmark)
class BookmarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'url', 'link_type',
                    'preview_image', 'created_at', 'updated_at']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
