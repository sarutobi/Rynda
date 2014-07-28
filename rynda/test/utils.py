# coding: utf-8
import string
import random

from factory.fuzzy import BaseFuzzyAttribute


class FuzzyText(BaseFuzzyAttribute):

    def __init__(self, length=20, chars=string.ascii_letters, **kwargs):
        super(FuzzyText, self).__init__(**kwargs)
        self.chars = tuple(chars)
        self.length = length

    def fuzz(self):
        return "".join(random.choice(self.chars) for x in xrange(self.length))
