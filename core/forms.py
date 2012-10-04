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

class OrganizationForm(forms.ModelForm):
    class Meta():
        model = Organization
        widgets = {'category': forms.CheckboxSelectMultiple(),}
        exclude = ('dateAdd', 'locationId')

    lat = forms.FloatField(widget = forms.HiddenInput, required = False)
    lon = forms.FloatField(widget = forms.HiddenInput, required = False)
    region = forms.ModelChoiceField(Region.objects.all(), label = 'Регион')
    address = forms.CharField(label = 'Адрес', widget = forms.TextInput(attrs={'size':'90'}), required = False)
   # contacts = forms.CharField(label = 'Контакты',widget = forms.TextInput(attrs={'size':'90'}))
   # phone = forms.CharField(label = 'Список телефонов',widget = forms.TextInput(attrs={'size':'90'}), required = False )
   # email = forms.CharField(label = 'Список email',widget = forms.TextInput(attrs={'size':'90'}), required = False)
   # site = forms.CharField(label = 'Список сайтов',widget = forms.TextInput(attrs={'size':'90'}), required = False)
   # category = forms.ModelMultipleChoiceField(Category.objects.all(), label = 'Категории', widget = forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        org = kwargs.get('instance', None)
        if org.pk:
            initial = {'region': org.region(),'lat':org.latitude(), 'lon':org.longtitude(),
                'address': org.address(), 'phone': ','.join(org.phone), 'email': ','.join(org.email),
                'site': ','.join(org.site),}
            kwargs['initial'] = initial
        super(OrganizationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        ce = self.cleaned_data
        org = self.instance
        # Сначала установим все поля, имеющие отношение непосредственно к организации
        org.phone = '{%s}' % ce['phone']
        org.email = '{%s}' % ce['email']
        org.site = '{%s}' % ce['site']

        if not org.pk:
            ''' Это новый профиль, поэтому сначала мы создадим необходимые объекты,
            а потом будем изменять параметры'''
            l = Location()
            r = ce['region']
            l.latitude = r.cityId.latitude
            l.longtitude = r.cityId.longtitude
            l.save()
            org.locationId = l
        org.region(ce['region'])
        org.address(ce['address'])
        if ce['lat'] != 0.0:
            org.latitude(ce['lat'])
        if ce['lon'] != 0.0:
            org.longtitude(ce['lon'])
        super(OrganizationForm, self).save(*args, **kwargs)

class SubdomainForm(forms.ModelForm):
    class Meta():
        model = Subdomain
        exclude = ('order', )

    def save(self, *args, **kwargs):
        sd = self.instance
        #sd.order = 1
        super(SubdomainForm, self).save(*args, **kwargs)
