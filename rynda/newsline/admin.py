# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'publish', )
    list_filter = ('status', 'publish')
    search_fields = ('title', 'post')

admin.site.register(Post, PostAdmin)
