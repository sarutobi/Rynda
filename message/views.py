# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView

from core.models import Region, Subdomain
from message.models import Message
from feed.models import FeedItem

from utils.tree import to_tree

from core.context_processors import subdomains_context, categories_context
from message.forms import MessageForm

def list(request):
    last_requests = Message.objects.filter(messageType=1,status__gt=1,
        status__lt=6).values('id', 'title', 'date_add')[:5]
    last_offers = Message.objects.filter(messageType=2,status__gt=1,
        status__lt=6).values('id', 'title','date_add')[:5]
    last_completed = Message.objects.filter(messageType=1,status=6)\
        .values('id', 'title','date_add')[:5]
    last_info = Message.objects.filter(messageType=3,status__gt=1,
        status__lt=6).values('id', 'title','date_add')[:5]
    last_feeds = FeedItem.objects.filter(feedId=3).values('id','link',
        'title','date')[:5]
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
            'messages': Message.approved.select_related('location', 'messageType', 'location__regionId').all()[:10],
        },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
    )


def requests(request):
    return render_to_response('all_messages.html',
        {
            'messages': Message.approved.select_related('location',\
            'messageType', 'location__regionId').filter(messageType=1)[:10],
        },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
    )

def offer(request):
    return render_to_response('all_messages.html',
        {
            'messages': Message.approved.select_related('location',\
            'messageType', 'location__regionId').filter(messageType=2)[:10],
        },
        context_instance=RequestContext(request,
            processors=[subdomains_context, categories_context])
    )



def add_request_form(request):
    return render_to_response('request_form.html',
        {
            'form': MessageForm(),
        },
        context_instance=RequestContext(request)
    )


class MessageView(DetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = "message"

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        sc = subdomains_context(self.request)
        for key in sc.keys():
            context[key] = sc[key]
        return context

def show_message(request, id):
    return render_to_response('message_details.html',
    {
        'message': Message.objects.get(id=id)
    },
    context_instance=RequestContext(request,
        processors=[subdomains_context,])
    )
