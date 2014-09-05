# -*- coding: utf-8 -*-

import dns.exception

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import django_filters
import floppyforms.__future__ as forms

from core.utils import validate_email_domain
from message.models import Category


class SimpleRegistrationForm(forms.Form):
    """
    Simple registration form, request only user name, email and password.
    """
    first_name = forms.CharField(
        max_length=30,
        label=_("First Name"))
    last_name = forms.CharField(
        max_length=30,
        label=_("Last Name"))
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(
        max_length=128, widget=forms.PasswordInput(),
        label=_("Password"))
    password2 = forms.CharField(
        max_length=128, widget=forms.PasswordInput(),
        label=_("Password(retype)"))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _("The password fields did not match"))
        return self.cleaned_data

    def clean_first_name(self):
        if len(self.cleaned_data['first_name'].strip()) == 0:
            raise forms.ValidationError(_('You must provide a first name!'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if len(self.cleaned_data['last_name'].strip()) == 0:
            raise forms.ValidationError(_('You must provide a last name!'))
        return self.cleaned_data['last_name']

    def clean_email(self):
        # TODO Use mailgun flanker
        existing = User.objects.filter(
            email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("This email already registered"))
        try:
            validate_email_domain(self.cleaned_data['email'])
        except dns.exception.DNSException, e:
            raise forms.ValidationError(_("Email seems to be wrong"))
        return self.cleaned_data['email']


class UserFilter(django_filters.FilterSet):
    """ Allow filtering user list """
    class Meta:
        model = User
        fields = ['category', 'q']
        order_by = (
            ('full_name', 'User Name'),
            ('date_joined', 'Date joined'),
        )

    category = django_filters.ModelMultipleChoiceFilter(
        name="category",
        label=_("Category"),
        widget=forms.CheckboxSelectMultiple(),
        queryset=Category.objects.all()
    )

    q = django_filters.CharFilter(
        name='message',
        label=_("Keywords"),
        lookup_type="icontains",
        widget=forms.SearchInput(),
    )

    def get_order_by(self, order_value):
        if order_value == "full_name":
            return ["last_name", "first_name", ]
        return super(UserFilter, self).get_order_by(order_value)
