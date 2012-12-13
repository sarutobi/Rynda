from django.conf.urls import patterns, include, url

from message.views import MessageView, CreateRequest

urlpatterns = patterns('',
    (r'^(?P<pk>\d+)$', MessageView.as_view()),
    url(r'^vse$', 'message.views.all'),
    url(r'^pomogite$', 'message.views.requests'),
    url(r'^pomogu$', 'message.views.offer'),
    ('^pomogite/dobavit', CreateRequest.as_view()),

)
