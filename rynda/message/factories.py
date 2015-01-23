# -*- coding: utf-8 -*-

import factory
from factory import django, fuzzy
from rynda.core.factories import FuzzyMultiPoint
from rynda.test.factories import UserFactory

from .models import Message


class MessageFactory(django.DjangoModelFactory):
    """ Factory for messages. """
    FACTORY_FOR = Message

    title = fuzzy.FuzzyText()
    message = fuzzy.FuzzyText(length=200)
    messageType = fuzzy.FuzzyChoice(
        (Message.REQUEST, Message.OFFER, ))
    is_anonymous = True
    allow_feedback = True
    is_virtual = fuzzy.FuzzyChoice((True, False))
    user = factory.SubFactory(UserFactory)
    source = fuzzy.FuzzyChoice(("", fuzzy.FuzzyText()))
    is_active = False
    is_important = False
    is_removed = False
    status = Message.NEW

    @factory.lazy_attribute
    def address(self):
        if not self.is_virtual:
            return fuzzy.FuzzyText()
        return ''

    @factory.lazy_attribute
    def location(self):
        if not self.is_virtual:
            return FuzzyMultiPoint().fuzz()
        return None

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)
