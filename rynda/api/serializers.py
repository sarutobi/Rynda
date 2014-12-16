# -*- coding: utf-8 -*-

import json

from rest_framework import serializers

from rynda.message.models import Message


class JSONField(serializers.Field):
    """ Read-only JSON field serializer """
    def from_native(self, value):
        try:
            val = json.loads(value)
        except TypeError:
            raise serializers.ValidationError(
                "Could not load json <{}>".format(value)
            )
        return val


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'title', 'message', 'messageType', 'date_add',
            'additional_info', 'location',
        )

    additional_info = JSONField()


class MapMessageSerializer(serializers.ModelSerializer):
    """ Serialize message data for map markers """
    class Meta:
        model = Message
        fields = ('id', 'title', 'messageType', 'messageType_name', 'location')

    messageType_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField('get_coordinates')

    def get_coordinates(self, obj):
        """ Converts generic geocollection to flat point list """
        coords = list()
        if obj.location is not None:
            for c in obj.location.coords:
                coords.append([c[1], c[0]])
        return coords

    def get_messageType_name(self, obj):
        return obj.get_messageType_display()
