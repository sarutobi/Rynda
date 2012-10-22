# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Region, Message, Subdomain
from core.utils import get_categories_tree
from feed.models import FeedItem

from utils.tree import to_tree

from core.context_processors import subdomains_context, categories_context
from message.forms import MessageForm

def list(request):
    last_requests = Message.objects.filter(messageType=1).values('id', 'title', 'dateAdd')[:5]
    last_offers = Message.objects.filter(messageType=1,status__gt=1, status__lt=6).values('id', 'title')[:5]
    last_completed = Message.objects.filter(messageType=1,status=6).values('id', 'title')[:5]
    last_info = Message.objects.filter(messageType=3,status__gt=1,status__lt=6).values('id', 'title')[:5]
    last_feeds = FeedItem.objects.filter(feedId=3).values('id', 'link', 'title', 'date')[:5]
    return render_to_response('index.html',
        { 'regions': Region.objects.all(),
          #'categories': cat_tree,
          'requests': last_requests,
          'offers': last_offers,
          'completed': last_completed,
          'info': last_info,
          'news': last_feeds,
        },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
        )


def all(request):
    return render_to_response('all_messages.html',
        {
            'messages': Message.objects.select_related().filter(status__gt=1)[:10],
        },
        context_instance=RequestContext(request)
    )

def add_request_form(request):
    return render_to_response('request_form.html',
        {
            'form': MessageForm(),
        },
        context_instance=RequestContext(request)
    )
