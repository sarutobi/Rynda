# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfile(UserAdmin):
    inlines = [ProfileInline, ]

admin.site.register(User, UserProfile)
