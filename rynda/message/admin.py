# coding: utf-8

from django.contrib import admin
from django.urls import reverse

from leaflet.admin import LeafletGeoAdmin

from .forms import AdminMessageForm
from .models import Message, Category


class MessageAdmin(LeafletGeoAdmin):
    list_display = (
        'title',
        'user',
        'messageType',
        'status',
        'date_add',
        'last_edit',
    )
    list_display_links = ('title', )

    list_filter = ('status', 'messageType',)

    readonly_fields = ('edit_key', 'date_add', 'last_edit', "user", "sender_ip",
                       'get_full_name', 'get_phone', 'get_email',)

    fieldsets = (
        ("Message", {
            'fields': (
                'title', 'message',
                ('status', 'messageType', 'allow_feedback'), )}),
        ("Category", {'fields': ('category',), 'classes': ('collapse',), }),
        ("Contact", {"fields": (('get_full_name', "is_anonymous"),
                                ('get_phone', 'get_email'), ("user", "sender_ip"), )}),
        ("Flags", {"fields": (("is_active", "is_removed", "is_important"),)}),
        ("Position", {"fields": ("address", "location", )})
    )
    form = AdminMessageForm

    def get_full_name(self, obj):
        full_name =   "%s %s" % (obj.additional_info.get('first_name', 'Anonymous'), obj.additional_info.get('last_name'))
        return full_name

    def get_phone(self, obj):
        return obj.additional_info.get("phone", "No phone")

    def get_email(self, obj):
        return obj.additional_info.get("email", "No email")

    get_full_name.short_description = 'Contact name'
    get_phone.short_description = 'Phone'
    get_email.short_description = 'Email'

    def has_add_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Message, MessageAdmin)
admin.site.register(Category, CategoryAdmin)
