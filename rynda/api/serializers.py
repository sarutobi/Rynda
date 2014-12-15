# -*- coding: utf-8 -*-

import json

from django.contrib.gis.geos import Point

from rest_framework import serializers

from rynda.message.models import Message
from rynda.geozones.models import Location


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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class CoordinatesSerializer(serializers.ModelSerializer):
    """ Serialize only coordinates from location """
    class Meta:
        model = Location

    coordinates = serializers.Field(source='coordinates.json')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'title', 'message', 'messageType', 'date_add',
            'additional_info', 'location',
        )

    additional_info = JSONField()
    # linked_location = LocationSerializer()


class MapMessageSerializer(serializers.ModelSerializer):
    """ Serialize message data for map markers """
    class Meta:
        model = Message
        fields = ('id', 'title', 'messageType', 'location')

    messageType = serializers.ChoiceField(source='get_messageType_display')
    location = serializers.SerializerMethodField('get_coordinates')

    def get_coordinates(self, obj):
        """ Converts generic geocollection to flat point list """
        coords = list()
        if obj.location is not None:
            for c in obj.location.coords:
                coords.append([c[1], c[0]])
        return coords
