# -*- coding: utf-8 -*-

from itertools import chain

from django.forms.widgets import (
    MultiWidget, CheckboxInput, CheckboxSelectMultiple)
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import CategoryGroup

#from utils.tree import to_tree


class CategoryTree(CheckboxSelectMultiple):

    def __init__(self, attrs=None):
        #import pdb;pdb.set_trace()
        self.root = CategoryGroup.objects.all()
        super(CategoryTree, self).__init__(attrs)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        for i, cat in enumerate(self.root):
            output.append(u'<ul class="no_list">')
            output.append("<li>%s</li>" % force_unicode(cat.name))
            for j, c in enumerate(cat.category_set.all()):
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(
                        final_attrs,
                        id='%s_%s%s' % (attrs['id'], i, j))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = CheckboxInput(
                    final_attrs,
                    check_test=lambda value: value in str_values)
                option_value = force_unicode(c.id)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(c.name))
                output.append(
                    u'<li><label%s class="label_show">%s %s</label></li>' % (
                        label_for, rendered_cb, option_label))
            output.append(u'</ul>')
        output.append(u'')
        return mark_safe(u'\n'.join(output))

