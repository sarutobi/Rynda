#-*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from message.models import Message
# from message.serializers import
from message.models import Category
from core.serializers import CategorySerializer

from .serializers import MessageSerializer, MapMessageSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'messages': reverse('api-messages-list', request=request),
        'categories': reverse('api-cat-list', request=request),
        'map-markers': reverse('get-map-markers', request=request),
    })


class MapMessageList(generics.ListAPIView):
    queryset = Message.objects.active().all()
    serializer_class = MapMessageSerializer


class MessagesList(generics.ListAPIView):
    queryset = Message.objects.active().all()
    serializer_class = MessageSerializer
    paginate_by = 10


class CategoryList(generics.ListAPIView):
    model = Category
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    model = Category
    serializer_class = CategorySerializer
