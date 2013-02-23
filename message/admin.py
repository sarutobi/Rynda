# coding: utf-8

from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
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

admin.site.register(Message, MessageAdmin)
