# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from core.widgets import CategoryTree
from geozones.forms import LocationField
from geozones.widgets import GeolocationWidget
from message.models import Message


class MessageForm(forms.ModelForm):
    ''' Base message form'''
    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType', 'subdomain',
            'category',
            'is_anonymous', 'allow_feedback',
            'location', )
        widgets = {
            'location': GeolocationWidget(),
            'category': CategoryTree(),
        }

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


class RequestForm(UserMessageForm):
    ''' Simple request form. '''

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.REQUEST

    def clean_messageType(self):
        return Message.REQUEST


class OfferForm(UserMessageForm):
    ''' Simple offer form. '''

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.OFFER

    def clean_messageType(self):
        return Message.OFFER


class InformationForm(UserMessageForm):
    ''' Simple information form. '''

    def __init__(self, *args, **kwargs):
        super(InformationForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.INFO

    def clean_messageType(self):
        return Message.INFO


class AdminMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.Select(),
            'location': GeolocationWidget(),
            'category': CategoryTree(),
        }

    def clean_messageType(self):
        return self.cleaned_data['message_type']

