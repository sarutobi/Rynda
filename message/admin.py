# coding: utf-8

from django.contrib import admin

from .models import Message
from .forms import AdminMessageForm


class MessageAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/libs/jquery-1.8.1.min.js',
            'js/libs/leaflet.js',
    #        'js/plugins.js',
            'js/rynda.js',
        )
    list_display = (
        'pk',
        'title',
        'subdomain',
        'messageType',
        'status',
        'date_add',
    )
    list_display_links = ('pk', 'title')
    list_filter = ('status',)
    form = AdminMessageForm

admin.site.register(Message, MessageAdmin)
