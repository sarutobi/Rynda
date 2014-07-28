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


