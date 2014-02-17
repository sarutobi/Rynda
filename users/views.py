# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

from core.views import RyndaFormView, RyndaListView
from users.forms import SimpleRegistrationForm
from users.models import create_new_user


class UserDetail(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'u'


class UserList(RyndaListView):
    template_name = 'userlist.html'
    context_object_name = 'users'
    queryset = User.objects.select_related().exclude(
        pk=settings.ANONYMOUS_USER_ID).filter(
        is_active=True).order_by('date_joined')
    paginator_url = '/user/page/'
    paginate_by = 10


class CreateUser(RyndaFormView):
    '''
    New user regiatration.
    If registration form is valid, create a new deactivated user,
    new user profile (via signal) and send activation email to user.
    '''
    template_name = 'registerform_simple.html'
    form_class = SimpleRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        ce = form.cleaned_data
        create_new_user(
            first_name=ce['first_name'],
            last_name=ce['last_name'],
            email=ce['email'],
            password=ce['password1'],
        )
        return redirect(self.success_url)


def activate_profile(request, pk, key):
    user = User.objects.get(id=pk)
    p = user.get_profile()
    if p.activCode == key:
        user.is_active = True
        user.save()
        p.activCode = ''
        p.save()
        redirect('/login')
    redirect('/')
