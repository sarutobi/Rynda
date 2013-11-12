# -*- coding: utf-8 -*-

import dns.exception

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from core.widgets import CategoryTree
from geozones.forms import LocationField
from geozones.widgets import GeolocationWidget
from message.models import Message, MessageType


class MessageForm(forms.ModelForm):
    ''' Base message form'''
    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType', 'subdomain',
            'category',
            'is_anonymous', 'allow_feedback',
            'georegion', 'location', 'address',)
        widgets = {
            'location': GeolocationWidget(),
            'category': CategoryTree(),
        }

    def __init__(self, *args, **kwargs):
        message_type = kwargs.pop('message_type', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if not message_type:
            raise ValidationError(_('You must provide message type for this form!'))
        self.fields['messageType'].initial = message_type

    location = LocationField(required=False)

    def clean_messageType(self):
        test = self.cleaned_data['messageType']
        if not test:
            raise ValidationError(_("Unknown message type!"))
        return test

    def clean_location(self):
        location = self.cleaned_data['location']
        if location is None:
            return ""
        elif isinstance(location, list):
            return 'POINT(%f %f)' % (location[0], location[1])
        return location

    def save(self, *args, **kwargs):
        return super(MessageForm, self).save(*args, **kwargs)


class UserMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.HiddenInput(),
            'location': GeolocationWidget(),
            'category': CategoryTree(),
        }

    def save(self, *args, **kwargs):
        return super(UserMessageForm, self).save(*args, **kwargs)


#class SimpleRequestForm(UserMessageForm):
#    ''' Simple request form. '''
#
#    def __init__(self, *args, **kwargs):
#        super(SimpleRequestForm, self).__init__(*args, **kwargs)
#        self.fields['messageType'].initial = MessageType.TYPE_REQUEST
#
#    def clean_messageType(self):
#        return MessageType.TYPE_REQUEST


class AdminMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.Select(),
            'location': GeolocationWidget(),
            'category': CategoryTree(),
        }

    def clean_messageType(self):
        return self.cleaned_data['message_type']
