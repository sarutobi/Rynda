#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from core.models import Infopage
from core.forms import InfoPageForm

def delete(request):
    pass

def update(request):
    pass

def edit(request):
    pass

def create(request):
    pass

def show(request, id = None):
    if id:
        page = Infopage.objects.get(id=id)
    else:
        page = None

    form = InfoPageForm(request.POST or None, instance = page)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('core.views.infopages.list'))
    return render_to_response('infopage/show.html',{
        'id': id,
        'form': form,
    }, context_instance = RequestContext(request))

def list(request):
    return render_to_response('infopage/list.html', {
        'pages': Infopage.objects.all(),
        #'list_name': 'Список информационных страниц',
        #'management_description': 'В этом разделе вы можете создавать и редактировать информационные страницы',
        #'create_command': 'show/infopage',
        #'create_description': 'Создать новую информационную страницу',
    }, context_instance = RequestContext(request))
