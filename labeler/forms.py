# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from .base import Translations, default_dict


def apply_to_form(fields, mapping):
    labels = mapping.get('labels', {})
    help_texts = mapping.get('help_texts', {})
    error_messages = mapping.get('error_messages', {})
    empty_labels = mapping.get('empty_labels', {})
    keys = set(list(labels) + list(help_texts) + list(error_messages) + list(empty_labels))
    for key in keys:
        label = labels.get(key)
        help_text = help_texts.get(key)
        error_dict = error_messages.get(key)
        empty_label = empty_labels.get(key)
        field = fields[key]
        if label is not None:
            field.label = label
        if help_text is not None:
            field.help_text = help_text
        if empty_label is not None:
            field.empty_label = empty_label
        if error_dict and field.error_messages is not None:
            field.error_messages.update(error_dict)


class FormTranslations(Translations):

    def __init__(self, labels=default_dict, help_texts=default_dict, empty_labels=default_dict,
                 error_messages=default_dict, errors=default_dict, messages=default_dict, **kwargs):
        if labels is not default_dict:
            kwargs['labels'] = labels
        if help_texts is not default_dict:
            kwargs['help_texts'] = help_texts
        if empty_labels is not default_dict:
            kwargs['empty_labels'] = empty_labels
        if error_messages is not default_dict:
            kwargs['error_messages'] = error_messages
        if errors is not default_dict:
            kwargs['errors'] = errors
        if messages is not default_dict:
            kwargs['messages'] = messages
        super(FormTranslations, self).__init__(**kwargs)

    def inject(self, form_class):
        apply_to_form(form_class.base_fields, self)
        return form_class

    @property
    def help_texts(self):
        return self.subdict('help_texts')

    @property
    def empty_labels(self):
        return self.subdict('empty_labels')
