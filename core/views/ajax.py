#-*- coding: utf-8 -*-

import hashlib
from datetime import datetime
import os
try:
    from PIL import Image
except:
    import Image

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.core import serializers
from django.db.models import Count
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

import settings
from core.models import Message, MessageType, Multimedia

def get_messages(request):
    first_row = request.GET['iDisplayStart'] or 0
    num_rows = request.GET['iDisplayLength'] or 10
    last_row = int(first_row) + int(num_rows)
    sEcho = request.GET['sEcho']
    if sEcho == '1':
        # Новый цикл отображения?
        if not request.session.get('sEcho'):
            # Да, сохраняем в сессии фильтры
            request.session['s_cond'] = request.GET.get('sSearch_3')
            request.session['s_site'] = request.GET.get('sSearch_2')
            request.session['s_type'] = request.GET.get('sSearch_1')
    else:
        # Нет, продолжаем работу
        request.session['s_cond'] = request.GET.get('sSearch_3')
        request.session['s_site'] = request.GET.get('sSearch_2')
        request.session['s_type'] = request.GET.get('sSearch_1')

    s_cond = request.session.get('s_cond')
    s_site = request.session.get('s_site')
    s_type = request.session.get('s_type')

    request.session['sEcho'] = sEcho

    mimetype = 'application/json'

    mes = Message.objects.all().select_related().select_related('multimedia__message')
    if s_cond:
        mes = mes.filter(status = int(s_cond))
    if s_site:
        mes = mes.filter(subdomain = int(s_site))
    if s_type:
        mes = mes.filter(messageType = int(s_type))
    total = mes.count()
    mes = mes.values('id', 'title', 'messageType__name', 'dateAdd', 'subdomain__title', 'status').annotate(mm_count = Count('multimedia__id'))[first_row:last_row]
    return render_to_response('message/messages_list.js',
        {'messages': mes,
         'total': total,
         'page': sEcho,
        },
        mimetype=mimetype)

def get_messages_filters(request):
    return render_to_response('message/message_filters.js',
        {'s_site': request.session.get('s_site', 0),
         's_cond': request.session.get('s_cond', 0),
         's_type': request.session.get('s_type', 0),
        },
        mimetype = 'application/json'
    )

def image_add(request):
    if request.method == "POST":
        if request.is_ajax():
            # the file is stored raw in the request
            upload = request
            is_raw = True
            # AJAX Upload will pass the filename in the querystring if it
            # is the "advanced" ajax upload
            try:
                filename = request.GET['qqfile']
            except KeyError:
                return HttpResponseBadRequest("AJAX request not valid")
        # not an ajax upload, so it was the "basic" iframe version with
        # submission via form
        else:
            is_raw = False
            if len(request.FILES) == 1:
                # FILES is a dictionary in Django but Ajax Upload gives
                # the uploaded file an ID based on a random number, so it
                # cannot be guessed here in the code. Rather than editing
                # Ajax Upload to pass the ID in the querystring, observe
                # that each upload is a separate request, so FILES should
                # only have one entry. Thus, we can just grab the first
                # (and only) value in the dict.
                upload = request.FILES.values()[0]
            else:
                raise Http404("Bad Upload")
            filename = upload.name
        msg_id = request.GET.get('msg_id')
        if not msg_id:
            raise Http404("Bad Upload")
        #Тупая проверка на суффиксы файла.
        allow_suffixes = ('gif', 'jpg', 'png')
        fSuffix = suffixes(filename.split('.')[-1])
        if not fSuffix in allow_suffixes:
            raise Http404("Bad upload")
        # Make file name based on original file name and current timestamp
        baseFileName = hashlib.sha1( "%s%s" % (filename, datetime.now().isoformat()) ).hexdigest()
        storeFileName = "%s.%s" % (baseFileName, fSuffix)
        thumbFileName = "%s_thumb.%s" % (baseFileName, fSuffix)
        storePath = os.path.join(settings.MEDIA_ROOT,storeFileName) 
        f = open(storePath, 'wb')
        _store_uploaded(f, upload, is_raw)
        f.close()
        #Предполагаем, что файл - картинка, пытаемся на его основе создать превью
        try:
            img = Image.open(storePath)
        except IOError:
            #XXX Unlink uploaded file
            raise Http404("Bad Upload")
        thumb = _make_thumb(img, 100)
        thumb.save(os.path.join(settings.MEDIA_ROOT, thumbFileName))
        # All is good, now store meta in database
        m = Multimedia(link_type = 1, 
                       message_id = msg_id, 
                       uri = "/static/photo/%s" % storeFileName,
                       thumb_uri = "/static/photo/%s" %thumbFileName
                       )
        m.save()
        img_id = m.id 
        ret_json = {'success': True, 
                    'img_id': img_id,
                    'img': storeFileName, 
                    'thumb': thumbFileName, 
                    'msg_id': msg_id, 
                    'media_url': settings.MEDIA_URL}
        return HttpResponse(json.dumps(ret_json, cls=DjangoJSONEncoder))
    return Http404("Bad request")

def _make_thumb(img, max_size):
    ''' Создание миниатюры для картинки'''
    (w, h) = img.size
    if w > max_size or h > max_size:
        if w > h:
            k = float(max_size) / w
        else:
            k = float(max_size) / h
        w = int(w * k)
        h = int(h * k)
    img = img.resize((w, h))
    return img

def suffixes(suffix):
    """ Нормализация суффикса файла"""
    suffix = suffix.lower()
    if suffix == 'jpeg':
        suffix = 'jpg'
    return suffix

def _store_uploaded(storage, upload, is_raw):
    ''' функция сохранения загруженного файла'''
    if is_raw:
        chunk = upload.read(10485760) # 10MB
        while len(chunk) > 0:
            storage.write(chunk)
            chunk = upload.read(10485760)
    else:
        for chunk in upload.chunks():
            storage.write(chunk)
