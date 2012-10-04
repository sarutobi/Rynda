# -*- coding: utf-8 -*-

from lxml import etree

from django.shortcuts import render_to_response
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from core.models import Message, MessageType, Multimedia, Subdomain, Region
from core.forms import MessageForm

from utils.views import paginator

m_status = {1: u'Новое',
            2: u'Не подтверждено',
            3: u'Подтверждено',
            4: u'В работе',
            6: u'Закрыто'}

def list(request, show_deleted=False):
    if show_deleted:
        session_var = 'trash_page'
    else:
        session_var = 'message_page'
    if not request.GET.get('page') and request.session.get(session_var): 
        #Мы пришли по ссылке без указания страницы, но в сессии страница сохранена
        return HttpResponseRedirect('%s?page=%s' % (request.path, request.session.get('page')))
    stats = Message.objects.values('messageType__name').annotate(Count('messageType')).order_by()
    messages = Message.objects.all().select_related().extra(select = {
        'mm_count': '''select count(id) from multimedia where message_id="Message".id''',
        'comments' : '''select count(*) from in_reply_to where message_id="Message".id''',
        'is_removed': '''flags & x'10'::bigint != 0''',
        }).select_related().values('id', 'title', 'messageType_id', 'messageType__name',\
        'dateAdd', 'subdomain__title', 'status', 'locationId__regionId__name', 'mm_count',\
        'comments', 'is_removed')
    if not show_deleted:
        messages = messages.extra(where=['flags&16=0'])
    else:
       messages = messages.extra(where=['flags&16=16'])

    pg = request.GET.get('page', request.session.get(session_var))
    msg_type = int(request.GET.get('msg_type', request.session.get('msg_type', 0) ))
    if msg_type > 0:
        messages = messages.filter(messageType = msg_type)

    msg_status = int(request.GET.get('msg_status', request.session.get('msg_status', 0) ))
    if msg_status > 0:
        messages = messages.filter(status = msg_status)
    region = int(request.GET.get('region', request.session.get('region', 0) ))
    if region > 0:
        messages = messages.filter(locationId__regionId = region)

    subdomain = int(request.GET.get('subdomain', request.session.get('subdomain', -1) ))
    if subdomain >= 0:
        messages = messages.filter(subdomain = subdomain)
    if subdomain != request.session.get('subdomain', -50) or region != request.session.get('region', -50) or msg_status != request.session.get('msg_status', -50) or msg_type != request.session.get('msg_type', -50):
        pg = 1
    request.session['msg_type'] = msg_type
    request.session['msg_status'] = msg_status
    request.session['subdomain'] = subdomain
    request.session['region'] = region
    pgr = Paginator(messages, 25)
    try:
        messages = pgr.page(pg)
    except PageNotAnInteger:
        messages = pgr.page(1)
        pg = 1
    except EmptyPage:
        messages = pgr.page(pgr.num_pages)
        pg = pgr.num_pages

    request.session[session_var] = pg
    for m in messages:
        m['m_status'] = m_status[m['status']]
    if show_deleted:
        url_list = 'trash_list'
    else:
        url_list = 'msg_list'
    return render_to_response('message/list.html',{
        'messages': messages,
        'url_list': url_list,
        'regions': Region.objects.values('id', 'name').all(),
        'total': pgr.count,
        'stats' : stats,
        'subdomains': Subdomain.objects.values('id', 'title').all(),
        'types': MessageType.objects.values('id', 'name').all(),
        'status': m_status,
        'region': region,
        'paginate': paginator(pgr.num_pages, page=pg),
        'type': msg_type,
        'cur_page':int(pg),
        'page': pgr.page(pg)}, context_instance = RequestContext(request))

def testCoffee(request):
    return render_to_response('treetest.html', context_instance = RequestContext(request))

def show(request, id):
    msg = Message.objects.select_related().select_related('locationId','multimedia__message', 'location__region').get(id=id)

    form = MessageForm(request.POST or None, instance = msg)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect("%s?page=%s" % ( reverse('core.views.messages.list'), request.session.get('page') ))
    return render_to_response('message/show.html', {
        'id' : id,
        'form': form,
        'dateAdd': msg.dateAdd,
        'dateModify': msg.dateModify,
        'sender': msg.get_sender(),
        'key': settings.GOOGLE_API_KEY,
        'anonymous': msg.anonymous(),
        'notes': msg.notes,
        'images': Multimedia.objects.filter(message = msg.id),
    }, context_instance = RequestContext(request))

def delete(request, id):
    try:
        m = Message.objects.get(id=id)
        m.flags = m.flags | 0x10
        m.save()
    except:
        pass
    page = request.session.get('page', 1)
    return HttpResponseRedirect('/list/messages?page=%s' % page)


def undelete(request, id):
    try:
        m = Message.objects.get(id=id)
        mask = ~(0x10)
        m.flags = m.flags & mask
        m.save()
    except:
        pass
    page = request.session.get('page', 1)
    return HttpResponseRedirect('/list/messages?page=%s' % page)

def remove_image(request, id):
    m = Multimedia.objects.values('id', 'message_id', 'uri', 'thumb_uri').get(id=id)
    #Multimedia.objects.delete(id=id)
    return HttpResponseRedirect('/show/message/%s' % m['message_id'])
