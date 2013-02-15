# -*- coding: utf-8 -*-

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from message.models import Message, MessageType
from core.models import Category
from core.widgets import CategoryTree
from geozones.models import Location, Region


class SimpleRequestForm(forms.ModelForm):
    '''
    Simple request form. This form is combined with model and flat form.
    It is possible to make this form only flat, 'cause this form functionality
    is cross-model.
    '''
    class Meta:
        model = Message
        widgets = {'messageType': forms.HiddenInput, }

    def __init__(self, *args, **kwargs):
        super(SimpleRequestForm, self).__init__(*args, **kwargs)
        self.fields['messageType'].initial = MessageType.TYPE_REQUEST
        self.fields['latitude'].initial = '55.75222'
        self.fields['longitude'].initial = '37.61556'

    # Location fields
    address = forms.CharField(required=True)
    latitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput, required=False)
    # XXX How to drop this ?
    region = forms.ModelChoiceField(
        Region.objects.all(),
        label=_("region"),
        required=False)

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
        return MessageType.TYPE_REQUEST

    def clean_address(self):
        address = self.cleaned_data['address']
        if address is None:
            raise ValidationError(_("You must provide an address"))
        return address

    def save(self, *args, **kwargs):
        l = Location(
            description=self.cleaned_data['address'],
            latitude=self.cleaned_data['latitude'],
            longitude=self.cleaned_data['longitude'])
        l.save()
        self.instance.location = l
        return super(SimpleRequestForm, self).save(*args, **kwargs)
#class RequestForm(forms.ModelForm):
#    class Meta:
#        model = Message
#        exclude = ('messageType', 'flags', 'status', 'date_add', 'last_edit',
#            'expired_date','location', 'sender', 'subdomain', 'edit_key',
#            'notes', 'user', '')
#        widgets = {'category': CategoryTree(tree=Category.objects.
#            filter(subdomain=None).values('id', 'name', 'parentId')),
#            'message': forms.Textarea(attrs={'rows': 5, 'cols': 5})
#        }
#
#    lat = forms.FloatField(widget=forms.HiddenInput)
#    lon = forms.FloatField(widget=forms.HiddenInput)
#    region = forms.ModelChoiceField(Region.objects.all(), label='Регион')
    #category = forms.ModelChoiceField(Category.objects.filter(subdomain=None)
    #    .exclude(parentId=None),widget=CategoryWidget())
#    messageType = forms.ModelChoiceField(MessageType.objects.filter(id__lt=5), label='Тип сообщения')
    #msgType = forms.ChoiceField(choices = Message.MESSAGE_TYPE, label = 'Тип сообщения')
#    address = forms.CharField(label='Адрес')
#    active = forms.BooleanField(label='Сообщение активно',required=False) #Флаг может быть в состоянии on/off
#    important = forms.BooleanField(label='Сообщение важно', required=False)#Флаг может быть в состоянии on/off

#    def __init__(self, *args, **kwargs):
#        msg = kwargs.get('instance',None)
#        if msg:
#            initial = {
#                'address': msg.address(),
#                'lat': msg.latitude(),
#                'lon': msg.longtitude(),
#                'active':msg.active(),
#                'important': msg.important(),
#                'region': msg.region(),
#                }
#            kwargs['initial'] = initial
#        super(MessageForm, self).__init__(*args, **kwargs)

#    def save(self, *args, **kwargs):
#        msg = self.instance
#        ce = self.cleaned_data
#        msg.latitude(ce['lat'])
#        msg.longtitude(ce['lon'])
#        msg.address(ce['address'])
#        msg.region( ce['region'])
#        msg.set_flag(Message.ACTIVE, ce['active'])
#        msg.set_flag(Message.IMPORTANT, ce['important'])
#        super(MessageForm, self).save(*args, **kwargs)

