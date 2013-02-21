# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


class GeolocationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.HiddenInput(),
            forms.HiddenInput(),
        )
        super(GeolocationWidget, self).__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return render_to_string(
            'geozones/widgets/geolocation.html',
            {
                'latitude': {
                    'html': rendered_widgets[0],
                    'label': _('latitude'), },
                'longitude': {
                    'html': rendered_widgets[1],
                    'label': _('longitude'), },
            }
        )

    def decompress(self, value):
        if value:
            return (value.latitude, value.longitude)
        return (None, None, None)

    class Media:
        js = (
            'geozones/l.control.geosearch.js',
            'geozones/l.geosearch.provider.google.js',
            'geozones/geolocation.js',
        )
        css = {
            'all': (
                'geozones/geolocation.css',
                'geozones/l.geosearch.css', )
        }
