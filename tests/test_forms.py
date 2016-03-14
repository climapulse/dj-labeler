# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from django import forms
from django.test import SimpleTestCase
from labeler import FormTranslations, resolve_dict_value


i18n_simple_issue_form = FormTranslations(
    labels={
        'name': 'Z Name',
        'description': 'Z Description',
        'issue_type': 'Z Type'
    },
    help_texts={
        'name': 'Keep it short please',
        'issue_type': 'Take a guess'
    },
    empty_labels={
        'issue_type': 'Pick one'
    },
    error_messages={
        'name': {
            'required': 'Come on! It says "Required" right below the input! Fill something in!'
        }
    },
    errors={
        'name': {
            'null': 'Sorry, we cannot handle the name "Null"'
        }
    },
    messages={
        'thankyou': 'Thanks'
    }
)


i18n_simple_issue_form_alt = FormTranslations(
    labels={
        'name': 'D Name',
        'description': 'D Description',
        'issue_type': 'D Type'
    },
    help_texts={
        'name': 'Yo, keep it short please',
        'issue_type': 'Please take a guess'
    },
    empty_labels={
        'issue_type': 'Just pick one'
    },
    error_messages={
        'name': {
            'required': 'Mate! It says "Required" right below the input! Fill something in!'
        }
    }
)


class SimpleIssueForm(forms.Form):
    name = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    issue_type = forms.TypedChoiceField(choices=[
        ('bug', 'Bug'), ('issue', 'Issue'), ('question', 'Question')
    ], required=False, widget=forms.RadioSelect)


class SimpleIssueFormTest(SimpleTestCase):

    def test_regular(self):
        form = i18n_simple_issue_form.inject(SimpleIssueForm)(data={})
        self.assertEqual(form.fields['name'].label, 'Z Name')
        self.assertEqual(form.fields['name'].help_text, 'Keep it short please')
        self.assertEqual(form.fields['description'].label, 'Z Description')
        self.assertFalse(form.fields['description'].help_text)
        self.assertEqual(form.fields['issue_type'].label, 'Z Type')
        self.assertEqual(form.fields['issue_type'].help_text, 'Take a guess')
        self.assertEqual(form.fields['issue_type'].empty_label, 'Pick one')
        form.is_valid()
        name_errors = form.errors['name']
        self.assertEqual(len(name_errors), 1)
        expected_error = i18n_simple_issue_form.resolve('error_messages.name.required')
        self.assertEqual(name_errors[0], expected_error)

    def test_alt(self):
        form = i18n_simple_issue_form_alt.inject(SimpleIssueForm)(data={})
        self.assertEqual(form.fields['name'].label, 'D Name')
        self.assertEqual(form.fields['name'].help_text, 'Yo, keep it short please')
        self.assertEqual(form.fields['description'].label, 'D Description')
        self.assertFalse(form.fields['description'].help_text)
        self.assertEqual(form.fields['issue_type'].label, 'D Type')
        self.assertEqual(form.fields['issue_type'].help_text, 'Please take a guess')
        self.assertEqual(form.fields['issue_type'].empty_label, 'Just pick one')
        form.is_valid()
        name_errors = form.errors['name']
        self.assertEqual(len(name_errors), 1)
        expected_error = i18n_simple_issue_form_alt.resolve('error_messages.name.required')
        self.assertEqual(name_errors[0], expected_error)


class FormTranslationsTest(SimpleTestCase):

    def test_messages(self):
        self.assertEqual('Thanks', i18n_simple_issue_form.messages['thankyou'])

    def test_help_texts(self):
        self.assertEqual('Keep it short please', i18n_simple_issue_form.help_texts['name'])

    def test_empty_labels(self):
        self.assertEqual('Pick one', i18n_simple_issue_form.empty_labels['issue_type'])
