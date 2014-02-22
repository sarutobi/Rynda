#-*- coding: utf-8 -*-

# from django.forms.fields import MultipleChoiceField
# from django.forms.widgets import CheckboxSelectMultiple
import floppyforms as forms


class CategoryChoiceField(forms.CheckboxSelectMultiple):
    template_name = 'category.html'
