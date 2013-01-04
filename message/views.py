# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from django.contrib.auth import logout

from core.models import Region, Subdomain
from message.models import Message
from feed.models import FeedItem

from utils.tree import to_tree

from core.context_processors import subdomains_context, categories_context
from core.mixins import SubdomainContextMixin, CategoryMixin
from core.views import RyndaCreateView, RyndaDetailView, RyndaListView

from message.forms import RequestForm

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

def logout_view(request):
    logout(request)
    return redirect('/')


class CreateRequest(CategoryMixin, RyndaCreateView):
    template_name = "request_form_simple.html"
    model = Message
    form_class = RequestForm

    def get_initial(self):
        '''Returns default values if user is authenticated'''
        initial = {}
        if self.request.user.is_authenticated():
            u = self.request.user
            initial['contact_first_name'] = u.first_name
            initial['contact_last_name'] = u.last_name
            initial['contact_mail'] = u.get_profile().email
        return initial


class CreateOffer(CategoryMixin, RyndaCreateView):
    template_name = "offer_form.html"
    model = Message
    form_class = RequestForm

class MessageView(RyndaDetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = "message"


class MessageList(RyndaListView):
    queryset = Message.approved.select_related('location', 'messageType', 'location__regionId').all()
    paginate_by = 10
    template_name = 'all_messages.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        print context['page_obj'].number
        sc = self.paginator(context['paginator'].num_pages, page=context['page_obj'].number)
        context['paginator_line'] = sc
        return context
