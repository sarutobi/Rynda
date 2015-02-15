# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from rynda.core.views import RyndaListView
from rynda.geozones.models import Region
from .forms import (RequestForm, OfferForm,
                    MessageSideFilter, MapMessageFilter)
from .models import Message

MAX_PANE_MESSAGES = 5


def generate_message_pane(pane_label, context_messages, link_to_continue=None):
    """ Dashboard message pane generator """
    has_more = len(context_messages) > MAX_PANE_MESSAGES
    context = {
        "messages": context_messages[:MAX_PANE_MESSAGES],
        "has_more": has_more,
        "helper_title": pane_label,
        "link_to_continue": link_to_continue,
    }
    return render_to_string("widgets/message_pane.html", context)


def list(request, slug='all'):
    """ Main page """
    last_requests = generate_message_pane(
        _("Help requests"),
        Message.objects.active().type_is(Message.REQUEST)[:MAX_PANE_MESSAGES + 1],
        reverse_lazy("messages-list"))
    last_offers = generate_message_pane(
        _("Offers to help"),
        Message.objects.active().type_is(Message.OFFER)[:MAX_PANE_MESSAGES + 1],
        reverse_lazy("messages-list"))
    last_completed = generate_message_pane(
        _("Successful connections"),
        Message.objects.type_is(
            Message.REQUEST).closed()[:MAX_PANE_MESSAGES + 1],
        "/message/pomogli")
    return render(
        request,
        'index.html',
        {
            'regions': Region.objects.filter(id__gt=0),
            'requests': last_requests,
            'offers': last_offers,
            'completed': last_completed,
            'filter': MapMessageFilter()
        },)


def logout_view(request):
    logout(request)
    return redirect('/')


class SaveGeoDataMixin():
    """ Store message and location """
    def form_valid(self, form):
        instance = form.save(commit=False)
        if self.request.user.is_authenticated():
            instance.user = self.request.user
        else:
            instance.user = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        instance.save()
        return redirect(self.success_url)


class CreateRequest(SaveGeoDataMixin, FormView):
    template_name = "request_form.html"
    model = Message
    form_class = RequestForm
    success_url = reverse_lazy('messages-list')

    def get_initial(self):
        initial = {}
        if self.request.user.is_authenticated():
            initial['contact_first_name'] = self.request.user.first_name
            initial['contact_last_name'] = self.request.user.last_name
            initial['contact_mail'] = self.request.user.email
            initial['contact_phone'] = self.request.user.profile.phones
        return initial


class CreateOffer(SaveGeoDataMixin, CreateView):
    template_name = "offer_form.html"
    model = Message
    form_class = OfferForm
    success_url = reverse_lazy('messages-list')


class MessageView(DetailView):
    model = Message
    template_name = "message_details.html"
    context_object_name = "message"


class MessageList(RyndaListView):
    queryset = Message.objects.active().prefetch_related('user', 'category').all()
    paginate_by = 10
    template_name = 'messages_list.html'
    context_object_name = 'messages'
    paginator_url = '/message/page/'
    list_title_short = _('Message list')

    def get_context_data(self, **kwargs):
        context = super(MessageList, self).get_context_data(**kwargs)
        context['filter'] = MessageSideFilter(self.request.GET, self.queryset)
        count = self.queryset.count()
        context['count'] = count
        return context


class ClosedMessageList(MessageList):
    queryset = Message.objects.closed().prefetch_related('user', 'category').all()
