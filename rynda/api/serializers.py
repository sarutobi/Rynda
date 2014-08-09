# -*- coding: utf-8 -*-

import json

from rest_framework import serializers

from message.models import Message
from geozones.models import Location


class JSONField(serializers.Field):
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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'title', 'message', 'messageType', 'date_add',
            'additional_info', 'linked_location',
        )

    additional_info = JSONField()
    linked_location = LocationSerializer()
