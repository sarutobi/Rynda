# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

from core.views import RyndaFormView, RyndaListView

from users.forms import SimpleRegistrationForm
from users.models import Users

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


class CreateUser(RyndaFormView):
    template_name = 'registerform_simple.html'
    #model = User
    form_class = SimpleRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        #print self.request.META['HTTP_HOST']
        user = User()
        ce = form.cleaned_data
        user.email = ce['email']
        user.login = ce['email']
        user.set_password(ce['password1'])
        user.save()
        #profile = Users.objects.create(user=user, ipAddr=self.request.META['REMOTE_ADDR'])
        #profile.user = user
        #profile.email = ce['email']
        #profile.ipAddr = vself.request.META['REMOTE_ADDR']
        #profile.save()
        return redirect(self.success_url)


def create_user(request):
    return render_to_response('registerform_simple.html',
        {'form': SimpleRegistrationForm(),}
    )
