# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from django.core.exceptions import FieldDoesNotExist
from django.test import SimpleTestCase
from labeler import ModelTranslations
from .models import Comment, Issue, IssueType, State, i18n_issue, i18n_issue_type


class ModelTest(SimpleTestCase):

    def test_issue_type(self):
        meta = IssueType._meta
        key = meta.get_field('key')
        self.assertEqual(key.verbose_name, 'label:Key')
        self.assertEqual(key.help_text, 'Technical key')
        label = meta.get_field('label')
        self.assertEqual(label.verbose_name, 'label:Label')
        self.assertEqual(label.help_text, 'Human-friendly label')
        self.assertEqual(meta.verbose_name, 'Type')
        self.assertEqual(meta.verbose_name_plural, 'Types')

    def test_state(self):
        meta = State._meta
        key = meta.get_field('key')
        self.assertEqual(key.verbose_name, 'state:Key')
        self.assertEqual(key.help_text, 'A technical key')
        label = meta.get_field('label')
        self.assertEqual(label.verbose_name, 'state:Label')
        self.assertEqual(label.help_text, 'A human-friendly label')
        end_state = meta.get_field('end_state')
        self.assertEqual(end_state.verbose_name, 'state:End state')
        self.assertEqual(end_state.help_text, 'Whether this state is and end state or not')
        self.assertEqual(meta.verbose_name, 'Issue state')
        self.assertEqual(meta.verbose_name_plural, 'Issue states')

    def test_issue_priorities(self):
        issue = Issue()
        priorities = i18n_issue['priorities']
        for value, label in priorities.items():
            issue.priority = value
            self.assertEqual(priorities[value], issue.get_priority_display())

    def test_no_such_field(self):
        new_translations = ModelTranslations(labels={'does_not_exist': 'Hey!'})
        try:
            new_translations.inject(State)
            self.fail('Expected an error')
        except FieldDoesNotExist:
            pass

    def test_comment(self):
        meta = Comment._meta
        content = meta.get_field('content')
        self.assertEqual(content.verbose_name, 'Comment')
        self.assertEqual(content.help_text, 'No profanity please')

    def test_errors(self):
        self.assertEqual('Please do not use profanity', i18n_issue_type.errors['no_profanity'])

    def test_error_messages(self):
        unique_message = IssueType._meta.get_field('key').error_messages['unique']
        self.assertEqual(unique_message, i18n_issue_type.resolve('error_messages.key.unique'))

    def test_messages(self):
        self.assertEqual('Thank you for reporting this issue', i18n_issue_type.messages['thankyou'])

    def test_help_texts(self):
        self.assertEqual('Technical key', i18n_issue_type.help_texts['key'])
