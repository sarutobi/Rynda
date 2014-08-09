# -*- coding: utf-8 -*-

from rest_framework import serializers

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'title', 'message', 'messageType', 'date_add',
        )
        # exclude = {'user', }

    user = serializers.PrimaryKeyRelatedField(required=False)
