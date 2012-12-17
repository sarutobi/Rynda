# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView

from users.models import Users

class UserDetail(DetailView):
    model = Users
    template_name = 'user_profile.html'
    context_object_name = 'u'
