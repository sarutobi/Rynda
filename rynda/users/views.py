# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView

from core.views import RyndaFormView, RyndaListView
from users.forms import SimpleRegistrationForm, UserFilter
from users.models import create_new_user, activate_user


class UserDetail(DetailView):
    model = User
    template_name = 'user_details.html'
    context_object_name = 'u'


class UserList(RyndaListView):
    template_name = 'user_list.html'
    context_object_name = 'users'
    queryset = User.objects.select_related().exclude(
        pk=settings.ANONYMOUS_USER_ID).filter(
            is_active=True).order_by('date_joined')
    list_title_short = _("User list")
    paginator_url = '/user/page/'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['filter'] = UserFilter(self.request.GET, self.queryset)
        count = self.queryset.count()
        context['count'] = count
        return context


class CreateUser(RyndaFormView):
    """
    New user registration.
    If registration form is valid, create a new deactivated user,
    new user profile (via signal) and send activation email to user.
    """
    template_name = 'registration_form.html'
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
        return render(
            self.request,
            "registration_success.html",
        )


def activate_profile(request, pk, key):
    user = User.objects.get(id=pk)
    if activate_user(user, key):
        # TODO Add correct message
        messages.add_message(request, messages.SUCCESS, "OK!")
        return redirect(reverse("user-login"))
    return redirect('/')
