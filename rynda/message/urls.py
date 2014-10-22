from django.conf.urls import patterns, url

from .views import MessageView, CreateRequest, MessageList,\
    CreateOffer

urlpatterns = patterns('',
    url(r'^$', MessageList.as_view(), name="messages-list"),
    url(r'^page/(?P<page>\d+)/$', MessageList.as_view(), name='message-list-paged'),
    url(r'^(?P<pk>\d+)$', MessageView.as_view(), name='message-details'),
 #   url(r'^pomogite$', 'message.views.requests'),
 #   url(r'^pomogu$', 'message.views.offer'),
    url('^pomogite/dobavit', CreateRequest.as_view(), name='message-create-request'),
    url('^pomogu/dobavit', CreateOffer.as_view(), name='message-create-offer'),
)
