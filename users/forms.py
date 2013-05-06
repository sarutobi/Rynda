# -*- coding: utf-8 -*-

import dns.resolver, dns.exception

from django import forms
from django.contrib.auth.models import User

from users.models import Profile


class SimpleRegistrationForm(forms.Form):
    '''
    Simple registration form, request only user name, email and password.
    '''
    first_name = forms.CharField(
        max_length=30,
        label="First Name")
    last_name = forms.CharField(
        max_length=30,
        label="Last Name")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(
        max_length=128, widget=forms.PasswordInput(),
        label="Password")
    password2 = forms.CharField(
        max_length=128, widget=forms.PasswordInput(),
        label="Password(retype)")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The password fields did not match")
        return self.cleaned_data

    def clean_first_name(self):
        if len(self.cleaned_data['first_name'].strip()) == 0:
            raise forms.ValidationError('You must provide a first name!')
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if len(self.cleaned_data['last_name'].strip()) == 0:
            raise forms.ValidationError('You must provide a last name!')
        return self.cleaned_data['last_name']

    def clean_email(self):
        existing = User.objects.filter(
            email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError("This email already registered")
        domain = self.cleaned_data['email'].split('@')[1]
        try:
            result = dns.resolver.query(domain, 'MX')
        except dns.exception.DNSException, e:
            raise forms.ValidationError(u"The domain %s could not be found" % domain)
        return self.cleaned_data['email']


class ForgotPasswordForm(forms.Form):
    '''
    Reset password form. Ask users email and, if this email is registered,
    send remember code to this email.
    '''
    email = forms.EmailField(required=True, label='')

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if not user.exists():
            raise forms.ValidationError('This email isn\'t registered')
        return self.cleaned_data['email']


class ResetPasswordForm(forms.Form):
    '''
    Validate resetting password code.
    '''
    #email = forms.EmailField(required=True, label='')
    code = forms.CharField(required=True, max_length=40, label='')

