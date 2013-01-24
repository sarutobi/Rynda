# coding: utf-8
import string
import random

def generate_string(str_len=6, src=string.ascii_lower):
    return "".join(random.choice(src) for x in xrange(str_len))
