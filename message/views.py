# -*- coding: utf-8 -*-
# Create your views here.

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from core.context_processors import categories_context, subdomains_context
from core.mixins import CategoryMixin, SubdomainContextMixin, MultipleFormsView
from core.models import Subdomain
from core.views import (RyndaCreateView, RyndaDetailView, RyndaFormView,
                        RyndaListView)
from feed.models import FeedItem
from geozones.forms import LocationForm
from geozones.models import Region
from message.forms import RequestForm
from message.models import Message, MessageIndexFilter, MessageSideFilter

MAX_PANE_MESSAGES = 5


def generate_message_pane(pane_label, context_messages, link_to_continue=None):
    """ Генерация виджета панели сообщений на главной странице """
    has_more = len(context_messages) > MAX_PANE_MESSAGES
    context = {
        "messages": context_messages[:MAX_PANE_MESSAGES],
        "has_more": has_more,
        "helper_title": pane_label,
        "link_to_continue": link_to_continue,
    }
    return render_to_string("widgets/message_pane.html", context)


def list(request, slug='all'):
    """ Главная страница """
    last_requests = generate_message_pane(
        "Просьбы о помощи",
        Message.objects.active().type_is(
            Message.REQUEST).values(
                'id', 'title', 'date_add')[:MAX_PANE_MESSAGES + 1],
        "/message/pomogite")
    last_offers = generate_message_pane(
        "Предложения помощи",
        Message.objects.active().type_is(
            Message.OFFER).values(
                'id', 'title', 'date_add')[:MAX_PANE_MESSAGES + 1],
        "/message/pomogu")
    last_completed = generate_message_pane(
        "Помощь оказана",
        Message.objects.type_is(
            Message.REQUEST).closed().values(
                'id', 'title', 'date_add')[:MAX_PANE_MESSAGES + 1],
        "/message/pomogli")
    # last_info = Message.objects.active().type_is(
        # Message.INFO).values('id', 'title', 'date_add')[:5]
    # last_feeds = FeedItem.objects.filter(feedId=3).values(
        # 'id', 'link', 'title', 'date')[:5]
    return render(
        request,
        'index.html',
        {
            'regions': Region.objects.filter(id__gt=0),
            #'categories': cat_tree,
            'filter': MessageIndexFilter(
                request.GET, Message.objects.active().list().all()),
            'requests': last_requests,
            'offers': last_offers,
            'completed': last_completed,
            # 'info': last_info,
            # 'news': last_feeds,
        },)
        # context_instance=RequestContext(
            # request,
            # processors=[subdomains_context, categories_context]))


def logout_view(request):
    logout(request)
    return redirect('/')


class CreateRequest(CategoryMixin, RyndaFormView):
    template_name = "request_form_simple.html"
    model = Message
    form_class = RequestForm
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
        else:
            instance.user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)
        instance.save()
        return redirect(self.success_url)


class CreateRequestM(MultipleFormsView):
    template_name = "request_form_simple.html"
    model = Message
    form_classes = {
        'message': RequestForm,
        'location': LocationForm,
    }
    success_url = reverse_lazy('message_list')

    def get_initial(self):
        initial = {}
        if self.request.user.is_authenticated():
            initial['contact_first_name'] = self.request.user.first_name
            initial['contact_last_name'] = self.request.user.last_name
            initial['contact_mail'] = self.request.user.email
            initial['contact_phone'] = self.request.user.profile.phones
        return initial

    def forms_valid(self, forms):
        import pdb; pdb.set_trace()
        location = forms['location'].save(commit=False)
        location.region_id = 64
        location.save()
        message = forms['message'].save(commit=False)
        message.linked_location = location
        if self.request.user.is_authenticated():
            message.user = self.request.user
        else:
            message.user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)
        message.save()
        return super(CreateRequestM, self).forms_valid(forms)


class CreateOffer(CategoryMixin, RyndaCreateView):
    template_name = "offer_form.html"
    model = Message
    form_class = RequestForm


class MessageView(RyndaDetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = "message"

    def get_context_data(self, **kwargs):
        context = super(RyndaDetailView, self).get_context_data(**kwargs)
        if self.allow_external():
            external = {'VK_APP_ID':  settings.VK_APP_ID, }
            context['external'] = external
        return context


class MessageList(RyndaListView):
    queryset = Message.objects.active().select_related().all().prefetch_related('category')
    paginate_by = 10
    template_name = 'all_messages.html'
    context_object_name = 'messages'
    paginator_url = '/message/page/'
    list_title_short = 'Список сообщений'

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        context['filter'] = MessageSideFilter(self.request.GET, self.queryset)
        count = self.queryset.count()
        context['count'] = count
        return context

    def get_queryset(self):
        return MessageSideFilter(self.request.GET, self.queryset)
