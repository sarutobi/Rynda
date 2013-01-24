# coding: utf-8

import unittest

from .utils import generate_string

class TestGenerateString(unittest.TestCase):
    '''Test string generator function'''
    def test_generate(self):
        gen_str = generate_string()
        self.assertEqual(6, len(gen_str))
        self.assertEqual(gen_str, gen_str.lower())
