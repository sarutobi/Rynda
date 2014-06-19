from django.conf.urls import patterns, url

from message.views import MessageView, CreateRequest, MessageList,\
    CreateOffer

urlpatterns = patterns('',
    url(r'^$', MessageList.as_view(), name="message_list"),
    url(r'^page/(?P<page>\d+)/$', MessageList.as_view()),
    (r'^(?P<pk>\d+)$', MessageView.as_view()),
 #   url(r'^pomogite$', 'message.views.requests'),
 #   url(r'^pomogu$', 'message.views.offer'),
    url('^pomogite/dobavit', CreateRequest.as_view(), name='create-request'),
    ('^pomogu/dobavit', CreateOffer.as_view()),
)
