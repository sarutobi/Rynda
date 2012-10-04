#coding: utf-8 -*-

from django.shortcuts import render_to_response

from users.models import Users

def list(request):
    first = request.GET.get('start', 0)
    length = request.GET.get('length', 10)
    last = int(first) + int(length)
    users = Users.objects.filter(id__gt=1).select_related().order_by('created')
    if request.GET.get('name'):
        name = request.GET['name'].strip()
        from django.db.models import Q
        users = users.filter(Q(metauser__lastName__icontains=name)|Q(metauser__firstName__icontains=name))
    users = users[first:last]
    total = Users.objects.filter(id__gt=1).count()
    return render_to_response('user_list.js', {'users': users,'total': total,}, mimetype='application/json')
