# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from core.models import Organization
from core.forms import OrganizationForm

def show(request, id = None):
    if id:
        instance = Organization.objects.get(id=id)
    else:
        instance = Organization()
    form = OrganizationForm(request.POST or None, instance = instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('core.views.organizations.list'))
    from django.conf import settings
    return render_to_response('organization/show.html', {
        'id': id,
        'form': form,
        'key': settings.GOOGLE_API_KEY,
    }, context_instance = RequestContext(request))

def list(request, idx = None ):
    if idx:
        total = Organization.objects.filter(name__startswith = idx[0])
        title = u"Список организаций, начинающихся на '%s'" % unicode(idx[0])
    else:
        total = Organization.objects.all()
        title = 'Список всех организаций'
    p = Paginator(total, 25)
    page = request.GET.get('page')
    try:
        orgs = p.page(page)
    except PageNotAnInteger:
        orgs = p.page(1)
    except EmptyPage:
        orgs = p.page(p.num_pages)
    except:
        orgs = p.page(1)


    return render_to_response('organization/list.html', {
        'orgs': orgs,
        'idx': Organization.NamesIndex(),
        'management_description': 'В этом разделе вы можете управлять профилями организаций',
        'list_name' : title,
        'create_command': 'show/organization/',#reverse('core.views.organizations.list'),
        'create_description': 'Создать профиль новой организации',
    }, context_instance = RequestContext(request))

def delete(request, id = None):
    id = int(id)
    Organization.objects.get(id=id).delete()
    return list(request)
