# coding: utf-8
import string
import random


def generate_string(str_len=6, src=string.ascii_lowercase):
    return "".join(random.choice(src) for x in xrange(str_len))


def lorem_ipsum(words_count=30):
    lorem = list([])
    for i in xrange(words_count):
        word_length = random.randint(4, 8)
        lorem.append(generate_string(str_len=word_length))
    return " ".join(lorem)
