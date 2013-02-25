# -*- coding: utf-8 -*-

from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message


class MapMessageSerializer(serializers.ModelSerializer):
    lat = serializers.Field(source='location.y')
    lon = serializers.Field(source='location.x')

    class Meta:
        model = Message
        fields = ['id', 'title', 'lat', 'lon', 'messageType']
