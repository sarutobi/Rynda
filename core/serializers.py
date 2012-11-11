# -*- coding: utf-8 -*-

from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parentId = serializers.RelatedField(source='parentId')

    class Meta:
        model = Category
        fields =  ('id', 'name', 'parentId')
