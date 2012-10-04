#-*- coding: utf-8 -*-

from django import template

register = template.Library()

LEADING_RANGE = TRAINLING_RANGE = 3
AJACENT_PAGES = 2
in_leading_range = in_trailing_range = False

@register.inclusion_tag('paginate.html', takes_context = True)
def paginator(context):
    c_p = context['page']
    min_a_p = c_p - AJACENT_PAGES
    if min_a_p < 1:
        min_a_p = 1
    max_a_p = c_p + AJACENT_PAGES
    if max_a_p > context['num_pages']:
        max_a_p = context['num_pages']


    if c_p > 1:
        previous_page = True
    if context['num_pages'] > c_p:
        next_page = True

    if c_p < 3: 
        in_leading_range = True

