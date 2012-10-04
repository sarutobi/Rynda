# -*- coding: utf-8 -*-

from django.db.models import Max, Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from core.models import Category, Subdomain
from core.forms import CategoryForm

def list(request):
    '''Отображение списка категорий в различных видах'''
    #Определяем фильтр по поддомену(странице атласа)
    try:
        sub = int(request.GET['p'])
    except:
        sub = None
    cats = Category.objects.filter(parentId = None)
    cats = cats.filter(Q(subdomain = sub) | Q(subdomain = None))
    # Формируем заголовок списка
    if not sub:
        header = 'Список общих категорий'
    else:
        header = u'Список категорий раздела %s' % Subdomain.objects.get(id=sub).name()
    return render_to_response('category/list.html',
        {'items': cats,
         'management_description': 'В этом разделе вы можете управлять имеющимися категориями.',
         'create_command': 'show/category/',
         'list_name': header,
         'create_description': 'Создать новую категорию',
         'pages': Subdomain.objects.all(),
         'current': sub,
        }, context_instance = RequestContext(request))

def show(request, id = None):
    '''Отображение полной информации одной категории'''
    if id:
        cat = Category.objects.get(id = id)
    else:
        cat = None
    form = CategoryForm(request.POST or None, instance = cat)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('core.views.categories.list'))
    return render_to_response('category/show.html',
        {'id': id,
         'form': form,
        }, context_instance = RequestContext(request))

def delete(request, id):
    '''Удаление категории. Все подкатегории удаляемой категории
    перемещаются на уровень выше.'''
    try:
        Category.objects.filter(parentId=id).update(parentId=None)
        Category.objects.get(id=id).delete()
    except:
        pass
    return HttpResponseRedirect(reverse('core.views.categories.list'))

def moveup(request):
    pass

def movedown(request):
    pass

