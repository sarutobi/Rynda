# -*- coding: utf-8 -*-

from django.views.generic.detail import DetailView

from django.contrib.auth.models import User

from core.views import RyndaListView


class UserDetail(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'u'

class UserList(RyndaListView):
    template_name = 'userlist.html'
    context_object_name = 'users'
    queryset = User.objects.select_related().filter(is_active=True).order_by('date_joined')
    paginator_url = '/user/page/'
    paginate_by = 10

