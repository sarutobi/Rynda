from django.conf.urls import url

from .views import MessageView, CreateRequest, MessageList,\
    CreateOffer, ClosedMessageList, message_added

urlpatterns = ['',
    url(r'^$', MessageList.as_view(), name="messages-list"),
    url(r'^page/(?P<page>\d+)/$', MessageList.as_view(), name='message-list-paged'),
    url(r'^(?P<pk>\d+)$', MessageView.as_view(), name='message-details'),
 #   url(r'^pomogite$', 'message.views.requests'),
 #   url(r'^pomogu$', 'message.views.offer'),
    url('^pomogite/dobavit', CreateRequest.as_view(), name='message-create-request'),
    url('^pomogu/dobavit', CreateOffer.as_view(), name='message-create-offer'),
    url('^pomogite/pomogli/$', ClosedMessageList.as_view(), name='closed-message-list'),
    url('^pomogite/pomogli/page/(?P<page>\d+)/$', ClosedMessageList.as_view()),
    url(r'^added/$', message_added, name='message-added',),
]
