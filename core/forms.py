# -*- coding: utf-8 -*-

from django import forms

from core.models import *

class InfoPageForm(forms.ModelForm):
    class Meta():
        model = Infopage


class MessageForm(forms.ModelForm):
    class Meta():
        model = Message
        exclude = ('flags','locationId', 'sender')
        widgets = {'category':forms.CheckboxSelectMultiple(), }

    lat = forms.FloatField(widget = forms.HiddenInput)
    lon = forms.FloatField(widget = forms.HiddenInput)
    region = forms.ModelChoiceField(Region.objects.all(), label = 'Регион')
    messageType = forms.ModelChoiceField(MessageType.objects.filter(id__lt = 5), label = 'Тип сообщения')
    #msgType = forms.ChoiceField(choices = Message.MESSAGE_TYPE, label = 'Тип сообщения')
    address = forms.CharField(label = 'Адрес')
    active = forms.BooleanField(label = 'Сообщение активно',required = False) #Флаг может быть в состоянии on/off
    important = forms.BooleanField(label = 'Сообщение важно', required = False)#Флаг может быть в состоянии on/off

    def __init__(self, *args, **kwargs):
        msg = kwargs.get('instance',None)
        initial = {'address': msg.address(),'lat': msg.latitude(), 'lon': msg.longtitude(),
            'active':msg.active(), 'important': msg.important(), 'region': msg.region(),
            }
        kwargs['initial'] = initial
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        msg = self.instance
        ce = self.cleaned_data
        msg.latitude(ce['lat'])
        msg.longtitude(ce['lon'])
        msg.address(ce['address'])
        msg.region( ce['region'])
        msg.set_flag(Message.ACTIVE, ce['active'])
        msg.set_flag(Message.IMPORTANT, ce['important'])
        super(MessageForm, self).save(*args, **kwargs)

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        widgets = {
            'description': forms.Textarea(attrs = {'rows':'20', 'cols':'90'}),
            'color': forms.TextInput(attrs = {'size': '7'}),
        }
        exclude = ('order',)

    def clean_parentId(self):
        parentId = self.cleaned_data['parentId']
        if parentId and self.instance.haveChildren():
            raise forms.ValidationError('Эта категория не может быть сделана вложенной')
        return parentId

class SubdomainForm(forms.ModelForm):
    class Meta():
        model = Subdomain
        exclude = ('order', )

    def save(self, *args, **kwargs):
        sd = self.instance
        #sd.order = 1
        super(SubdomainForm, self).save(*args, **kwargs)
