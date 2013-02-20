# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import GeolocationWidget


class LocationField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        self.widget = GeolocationWidget()
        fields = (
            forms.DecimalField(label=_('latitude')),
            forms.DecimalField(label=_('llongitude')),
            forms.CharField(max_length=200, label=_('address'))
        )
        super(LocationField, self).__init__(fields, required=True)

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""


class LocationForm(forms.Form):
    location = LocationField()

    def get_latitude(self):
        return self.location.fields[0]

    def get_longitude(self):
        return self.location.fields[1]

    def get_address(self):
        return self.location.fields[2]
