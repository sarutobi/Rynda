# coding: utf-8

import unittest

from test.utils import generate_string, lorem_ipsum

class TestGenerateString(unittest.TestCase):
    '''Test string generator function'''
    def test_generate(self):
        gen_str = generate_string()
        self.assertEqual(6, len(gen_str))
        self.assertEqual(gen_str, gen_str.lower())

    def test_lorem_ipsum(self):
        lorem = lorem_ipsum()
        self.assertIsNotNone(lorem)
        lorem_len = len(lorem.split(" "))
        self.assertTrue(lorem_len >= 20)
        self.assertTrue(lorem_len <= 60)
