# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Region, Category, Message, Subdomain
from feed.models import FeedItem

from utils.tree import to_tree

def list(request):
    #cat_tree = to_tree(Category.objects.all())
    cat_tree = Category.objects.filter(parentId=None)
    last_requests = Message.objects.filter(messageType=1).values('id', 'title', 'dateAdd')[:5]
    last_offers = Message.objects.filter(messageType=1,status__gt=1, status__lt=6).values('id', 'title')[:5]
    last_completed = Message.objects.filter(messageType=1,status=6).values('id', 'title')[:5]
    last_info = Message.objects.filter(messageType=3,status__gt=1,status__lt=6).values('id', 'title')[:5]
    last_feeds = FeedItem.objects.filter(feedId=3).values('id', 'link', 'title', 'date')[:5] 
    return render_to_response('index.html',
        { 'regions': Region.objects.all(),
          'categories': cat_tree,
          'requests': last_requests,
          'offers': last_offers,
          'completed': last_completed,
          'info': last_info,
          'news': last_feeds,
          'subdomains': Subdomain.objects.all(),
        },
        context_instance=RequestContext(request))


def all(request):
    return render_to_response('all_messages.html',
        {
            'messages': Message.objects.filter(status__gt=1).select_related()[:10],
        },
        context_instance=RequestContext(request) 
    )
