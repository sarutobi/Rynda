# coding: utf-8

from django import forms

from leaflet.forms.widgets import LeafletWidget

from .models import Location


class LocationForm(forms.ModelForm):
    class Meta():
        model = Location
        fields = ['name', 'description', 'coordinates', ]
        widgets = {'coordinates': LeafletWidget(), }
