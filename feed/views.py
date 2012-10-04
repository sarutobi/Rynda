#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from feed.models import *
# Управление подписками для лент RSS

def listFeeds(request):
    return render_to_response('feed/feeds.html',
        {'feeds': Feed.objects.all(),
		'list_name': 'Список новостных лент',
        'management_description': 'В этом разделе вы можете создавать и редактировать ленты новостей',
        }, context_instance = RequestContext(request)
    )

def editFeed(request, feedId = None):
    pass

def feedContent(request, feedId):
    content = FeedItem. objects.filter(feedId = feedId)
    return render_to_response('feed/content.html',
        {'content': content,

        }, context_instance = RequestContext(request)
    )

