# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from django.test import SimpleTestCase
from labeler import resolve_dict_value, Translations


class ResolveDictValueTest(SimpleTestCase):

    def test_empty(self):
        self.assertTrue(resolve_dict_value({}, 'abc') is None)

    def test_not_nested(self):
        self.assertTrue(resolve_dict_value({'abc.xyz': 1}, 'abc') is None)

    def test_nothing(self):
        self.assertRaises(AttributeError, resolve_dict_value, {'abc': 1}, 'abc.xyz')

    def test_match(self):
        xyz = {'something': 'else'}
        abc = {'zyx': 1, 'xyz': xyz}
        values = {'abc': abc}
        self.assertEqual(resolve_dict_value(values, 'abc'), abc)
        self.assertEqual(resolve_dict_value(values, 'abc.zyx'), 1)
        self.assertEqual(resolve_dict_value(values, 'abc.xyz'), xyz)


class TranslationTest(SimpleTestCase):

    def test_subdict(self):
        self.assertDictEqual(dict(b=123), Translations(a=dict(b=123)).subdict('a'))
        self.assertDictEqual({}, Translations(a=123).subdict('b'))

    def test_labels(self):
        labels = dict(greeting='Hello', who='World')
        self.assertDictEqual(labels, Translations(labels=labels, errors={'a': 'Error'}).labels)
        self.assertDictEqual({}, Translations(errors={'a': 'Error'}).labels)

    def test_errors(self):
        errors = dict(invalid='Invalid', required='Required')
        self.assertDictEqual(errors, Translations(errors=errors).errors)
        self.assertDictEqual({}, Translations().errors)

    def test_messages(self):
        messages = dict(invalid='Invalid', required='Required')
        self.assertDictEqual(messages, Translations(messages=messages).messages)
        self.assertDictEqual({}, Translations().messages)
