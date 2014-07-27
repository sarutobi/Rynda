# coding: utf-8

from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
