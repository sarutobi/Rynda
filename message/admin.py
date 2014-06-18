# coding: utf-8

from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin

from .forms import AdminMessageForm
from .models import Message


class MessageAdmin(LeafletGeoAdmin):
    # class Media:
        # js = (
            # 'js/libs/jquery-1.8.1.min.js',
            # 'js/libs/leaflet.js',
            # 'js/plugins.js',
            # 'js/rynda.js',
        # )
    list_display = (
        'title',
        'subdomain',
        'user',
        'messageType',
        'status',
        'date_add',
        'last_edit',
    )
    list_display_links = ('title', )
    list_filter = ('status', 'messageType',)
    readonly_fields = ('edit_key', 'date_add', 'last_edit',)
    # fieldsets = (
        # ("Message", {'fields': ('title', 'message', )}),
        # ("Category", {'fields': ('category',), 'classes': ('collapse'), }),
        # ("Contact", {"fields": ("additional_info",)}),
        # ("Flags", {"fields": ("is_active", )})
    # )
    # form = AdminMessageForm

admin.site.register(Message, MessageAdmin)
