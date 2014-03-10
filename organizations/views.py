# -*- coding: utf-8 -*-

from django.shortcuts import render


def not_implemented(request):
    return render(
        request,
        'not_implemented.html',)
