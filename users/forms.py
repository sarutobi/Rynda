# -*- coding: utf-8 -*-

from users.models import Users
from django import forms


class SimpleRegistrationForm(forms.Form):
    '''
    Simple registration form, request only user email and password.
    '''
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(),
        label="Password")
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(),
        label="Password(retype)")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The password fields did not match")
        return self.cleaned_data

    def clean_email(self):
        existing = Users.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError("This email already registered")
        return self.cleaned_data['email']
