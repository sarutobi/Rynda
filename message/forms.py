# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import floppyforms as forms

from category.fields import CategoryChoiceField
from message.models import Message


class VirtualMessageFormMixin(forms.ModelForm):

    """ Виртуальные сообщения """

    def __init__(self, *args, **kwargs):
        super(VirtualMessageFormMixin, self).__init__(*args, **kwargs)
        self.fields['is_virtual'] = forms.BooleanField(default=True)

    def clean_isvirtual(self):
        return True

    def clean_location(self):
        return None


class MessageForm(forms.ModelForm):

    """ Базовая форма ввода сообщения """

    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType', 'subdomain',
            'category',
            'is_anonymous', 'allow_feedback',
        )
        widgets = {
            'category': CategoryChoiceField()
        }

    def clean_messageType(self):
        test = self.cleaned_data['messageType']
        if not test:
            raise ValidationError(_("Unknown message type!"))
        return test


class UserMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.HiddenInput(),
            'category': CategoryChoiceField(),
        }

    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    email = forms.EmailField(label=_('Contact email'))
    phone = forms.CharField(label=_('Contact phone'))


class RequestForm(UserMessageForm):
    """ Simple request form. """

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.REQUEST

    def clean_messageType(self):
        return Message.REQUEST


class OfferForm(UserMessageForm):
    """ Simple offer form. """

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.OFFER

    def clean_messageType(self):
        return Message.OFFER


class InformationForm(UserMessageForm):
    """ Simple information form. """

    def __init__(self, *args, **kwargs):
        super(InformationForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = Message.INFO

    def clean_messageType(self):
        return Message.INFO


class AdminMessageForm(MessageForm):
    class Meta(MessageForm.Meta):
        widgets = {
            'messageType': forms.Select(),
            'category': CategoryChoiceField(),
        }

    def clean_messageType(self):
        return self.cleaned_data['message_type']
