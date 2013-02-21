# -*- coding: utf-8 -*-

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from core.models import Category
from core.widgets import CategoryTree
from geozones.forms import LocationField
from geozones.models import Location, Region
from geozones.widgets import GeolocationWidget
from message.models import Message, MessageType


class MessageForm(forms.ModelForm):
    ''' Base message form'''
    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType',
            'contact_first_name', 'contact_last_name',
            'contact_mail', 'contact_phone',
            'georegion', 'location')
        widgets = {
            'messageType': forms.HiddenInput(),
            'location': GeolocationWidget()
        }

    location = LocationField(required=False)

    def clean_status(self):
        status = self.cleaned_data['status']
        if status is None:
            return self.fields['status'].initial
        return status

    def clean_flags(self):
        flags = self.cleaned_data['flags']
        if flags is None:
            return self.fields['flags'].initial
        return flags

    def clean_messageType(self):
        raise NotImplementedError('You must overwrite this method!')

    def clean_location(self):
        location = self.cleaned_data['location']
        if location is None:
            return ""
        elif isinstance(location, list):
            return 'POINT(%f %f)' % (location[0], location[1])
        return location

    def save(self, *args, **kwargs):
        return super(MessageForm, self).save(*args, **kwargs)


class SimpleRequestForm(MessageForm):
    ''' Simple request form. '''

    def __init__(self, *args, **kwargs):
        super(SimpleRequestForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = MessageType.TYPE_REQUEST

    def clean_messageType(self):
        return MessageType.TYPE_REQUEST
