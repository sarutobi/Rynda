# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Message, Comment, MessageComment

def list(request, msg_id):
    msg = Message.objects.values('title', 'message').get(id=msg_id)
    cmts = MessageComment.objects.select_related().filter(message_id = msg_id).order_by('id')
    return render_to_response('comments/list.html', {'comments': cmts, 'msg': msg},\
        context_instance = RequestContext(request))

def set_status(request, comment_id, new_status):
    c = Comment.objects.get(id = comment_id)
    c.status = new_status
    c.save()
    cmts = MessageComment.objects.select_related().filter(message_id = c.comment.message_id).order_by('id')
    return render_to_response('comments/list.html', {'comments': cmts}, context_instance = RequestContext(request))


def latest(request):
    comments = MessageComment.objects.select_related('comment', 'message').all().order_by('-comment__dateAdd')[:30]
    return render_to_response('comments/latest.html', {'comments': comments, },
        context_instance=RequestContext(request))
