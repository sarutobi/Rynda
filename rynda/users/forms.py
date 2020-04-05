# -*- coding: utf-8 -*-

import dns.exception

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import django_filters
#  import floppyforms.__future__ as forms
from django import forms

from rynda.core.utils import validate_email_domain
from rynda.message.models import Category
from .models import Profile


class SimpleRegistrationForm(forms.Form):
    """
    Simple registration form, request only user name, email and password.
    """
    first_name = forms.CharField(
        max_length=30,
        label=_("First name"))
    last_name = forms.CharField(
        max_length=30,
        label=_("Last name"))
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
        except dns.exception.DNSException:
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
        #  widget=forms.SearchInput(),
    )

    def get_order_by(self, order_value):
        if order_value == "full_name":
            return ["last_name", "first_name", ]
        return super(UserFilter, self).get_order_by(order_value)

    def get_ordering_field(self):
        if self._meta.order_by:
            if isinstance(self._meta.order_by, (list, tuple)):
                if isinstance(self._meta.order_by[0], (list, tuple)):
                    # e.g. (('field', 'Display name'), ...)
                    choices = [(f[0], f[1]) for f in self._meta.order_by]
                else:
                    choices = [(f, _('%s (descending)' % capfirst(f[1:])) if f[0] == '-' else capfirst(f))
                               for f in self._meta.order_by]
            else:
                # add asc and desc field names
                # use the filter's label if provided
                choices = []
                for f, fltr in self.filters.items():
                    choices.extend([
                        (fltr.name or f, fltr.label or capfirst(f)),
                        ("-%s" % (fltr.name or f), _('%s (descending)' % (fltr.label or capfirst(f))))
                    ])
            return forms.ChoiceField(label="Ordering", required=False,
                                     choices=choices)


class EditProfileForm(forms.ModelForm):
    """ Allow editing user profile """
    class Meta:
        model = Profile
        fields = ('is_public', 'about_me', 'birthday', 'gender')
