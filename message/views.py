# -*- coding: utf-8 -*-
# Create your views here.

from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from core.context_processors import subdomains_context, categories_context
from core.mixins import SubdomainContextMixin, CategoryMixin
from core.models import Subdomain
from core.views import (
    RyndaCreateView, RyndaDetailView, RyndaListView, RyndaFormView)
from geozones.models import Region
from feed.models import FeedItem

from message.forms import SimpleRequestForm
from message.models import (
    Message, MessageType,
    MessageSideFilter, MessageIndexFilter)


def list(request, slug='all'):
    last_requests = Message.objects.active().type_is(
        MessageType.TYPE_REQUEST).values('id', 'title', 'date_add')[:5]
    last_offers = Message.objects.active().type_is(
        MessageType.TYPE_OFFER).values('id', 'title', 'date_add')[:5]
    last_completed = Message.objects.type_is(
        MessageType.TYPE_REQUEST).closed().values('id', 'title', 'date_add')[:5]
    last_info = Message.objects.active().type_is(
        MessageType.TYPE_INFO).values('id', 'title', 'date_add')[:5]
    last_feeds = FeedItem.objects.filter(feedId=3).values(
        'id', 'link', 'title', 'date')[:5]
    return render_to_response(
        'index.html', {
            'regions': Region.objects.filter(id__gt=0),
            #'categories': cat_tree,
            'filter': MessageIndexFilter(
                request.GET, Message.objects.active().list().all()),
            'requests': last_requests,
            'offers': last_offers,
            'completed': last_completed,
            'info': last_info,
            'news': last_feeds, },
        context_instance=RequestContext(
            request,
            processors=[subdomains_context, categories_context]))


def logout_view(request):
    logout(request)
    return redirect('/')


class CreateRequest(CategoryMixin, RyndaFormView):
    template_name = "request_form_simple.html"
    model = Message
    form_class = SimpleRequestForm
    success_url = reverse_lazy('message_list')

    def get_initial(self):
        initial = {}
        if self.request.user.is_authenticated():
            initial['contact_first_name'] = self.request.user.first_name
            initial['contact_last_name'] = self.request.user.last_name
            initial['contact_mail'] = self.request.user.email
            initial['contact_phone'] = self.request.user.profile.phones
        return initial

    def form_valid(self, form):
        instance = form.save(commit=False)
        if self.request.user.is_authenticated():
            instance.user = self.request.user
        instance.save()
        return redirect(self.success_url)


class CreateOffer(CategoryMixin, RyndaCreateView):
    template_name = "offer_form.html"
    model = Message
    form_class = SimpleRequestForm


class MessageView(RyndaDetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = "message"


class MessageList(RyndaListView):
    queryset = Message.objects.active().list().all()
    paginate_by = 10
    template_name = 'all_messages.html'
    context_object_name = 'messages'
    paginator_url = '/message/page/'
    list_title_short = 'Список сообщений'

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        context['filter'] = MessageSideFilter(self.request.GET, self.queryset)
        return context

    def get_queryset(self):
        return MessageSideFilter(self.request.GET, self.queryset)
