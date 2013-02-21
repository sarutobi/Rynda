# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import GeolocationWidget


class LocationField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        self.widget = GeolocationWidget()
        fields = (
            forms.DecimalField(required=False, label=_('latitude')),
            forms.DecimalField(required=False, label=_('longitude')),
        )
        super(LocationField, self).__init__(fields, required=False)

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""

