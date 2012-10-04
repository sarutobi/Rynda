# -*- coding: utf-8 -*-

from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.models import Users

def list(request):
    users = Users.objects.values('id', 'first_name', 'last_name', 'created', 'active', 'flags','email', 'lastLogin').select_related().all()
    paginator = Paginator(users, 20)

    pg = request.GET.get('page', 1)
    try:
        page = paginator.page(pg)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    c_num = page.start_index()
    for i in page:
        i['created'] = datetime.fromtimestamp(i['created'])
        i['lastLogin'] = datetime.fromtimestamp(i['lastLogin'])
        i['number'] = c_num
        c_num += 1
    return render_to_response('users_list.html', {'users': page,'cur_page':int(pg), 'pager': paginator.page_range,},context_instance = RequestContext(request))
