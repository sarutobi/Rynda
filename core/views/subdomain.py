#-*- coding: utf-8 -*-
#Функции видов для работы с поддоменами сайта

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from core.forms import SubdomainForm
from core.models import Subdomain

def list(request):
    return render_to_response('subdomain/list.html', {
        'items': Subdomain.objects.all(),
        'management_description': "В этом разделе вы можете управлять поддоменами проекта",
		'list_name': 'Субдомены',

        }, context_instance = RequestContext(request))

def show(request, id = None):
    if id:
        sub = Subdomain.objects.get(id=id)
    else:
        sub = None
    form = SubdomainForm(request.POST or None, instance = sub)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('core.views.subdomain.list'))
    return render_to_response('subdomain/show.html', {
        'form': form,
        'id' : id,
        }, context_instance = RequestContext(request))
