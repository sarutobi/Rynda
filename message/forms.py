# -*- coding: utf-8 -*-

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from core.models import CategoryGroup
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
            'title', 'message', 'messageType', 'subdomain',
            'contact_first_name', 'contact_last_name',
            'contact_mail', 'contact_phone',
            'category',
            'is_anonymous', 'allow_feedback',
            'georegion', 'location', 'address')
        widgets = {
            'messageType': forms.HiddenInput(),
            'location': GeolocationWidget(),
            'category': CategoryTree(cat_groups=CategoryGroup.objects.all()),
        }

    location = LocationField(required=False)

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
