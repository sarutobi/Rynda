# -*- coding: utf-8 -*-

import factory
from factory import django, fuzzy
from rynda.test.factories import UserFactory

from rynda.geozones.factories import LocationFactory
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
    def linked_location(self):
        if self.is_virtual:
            ret = None
        else:
            ret = LocationFactory()
        return ret

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)
