# coding: utf-8

from django.contrib import admin
from django.urls import reverse

#  from leaflet.admin import LeafletGeoAdmin

# from .forms import AdminMessageForm
from .models import Message, Category


def get_full_name(obj):
    return "%s %s" % (obj.additional_info['first_name'], obj.additional_info['last_name'])


def get_phone(obj):
    return obj.additional_info.get("phone", "No phone")


def get_email(obj):
    return obj.additional_info.get("email", "No email")

get_full_name.short_description = 'Contact name'
get_phone.short_description = 'Phone'
get_email.short_description = 'Email'


#  class MessageAdmin(LeafletGeoAdmin):
    #  list_display = (
        #  'title',
        #  'user',
        #  'messageType',
        #  'status',
        #  'date_add',
        #  'last_edit',
    #  )
    #  list_display_links = ('title', )
    #  list_filter = ('status', 'messageType',)
    #  readonly_fields = ('edit_key', 'date_add', 'last_edit',
                       #  get_full_name, get_phone, get_email,
                       #  'user', 'sender_ip', )
    #  fieldsets = (
        #  ("Message", {
            #  'fields': (
                #  'title', 'message',
                #  ('status', 'messageType', 'allow_feedback'), )}),
        #  ("Category", {'fields': ('category',), 'classes': ('collapse',), }),
        #  ("Contact", {"fields": ((get_full_name, "is_anonymous"),
                                #  (get_phone, get_email), ("user", "sender_ip"), )}),
        #  ("Flags", {"fields": (("is_active", "is_removed", "is_important"),)}),
        #  ("Position", {"fields": ("address", "location", )})
    #  )
    #  # form = AdminMessageForm


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

#  admin.site.register(Message, MessageAdmin)
admin.site.register(Category, CategoryAdmin)
