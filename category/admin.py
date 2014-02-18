# coding: utf-8

from django.contrib import admin

from .models import Category, CategoryGroup


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)


class CategoryGroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(CategoryGroup, CategoryGroupAdmin)
