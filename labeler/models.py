# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from .base import Translations, default_dict, default_str


def apply_to_model(model_class, mapping):
    meta = model_class._meta
    verbose_names = mapping.get('labels', {})
    help_texts = mapping.get('help_texts', {})
    keys = set(list(verbose_names.keys()) + list(help_texts.keys()))
    for key in keys:
        verbose_name = verbose_names.get(key)
        help_text = help_texts.get(key)
        field = meta.get_field(key)
        if verbose_name:
            field.verbose_name = verbose_name
        if help_text:
            field.help_text = help_text
    singular = mapping.get('name')
    plural = mapping.get('name_plural')
    if singular:
        meta.verbose_name = singular
    if plural:
        meta.verbose_name_plural = plural


class ModelTranslations(Translations):
    """Translations dict for Django models.

    Provides an ``inject`` method you can use as a decorator your Django models and a customized ``__init__``
    to allow autocompletion and hinting in IDEs.

    """

    def __init__(self, labels=default_dict, help_texts=default_dict, name=default_str, name_plural=default_str,
                 errors=default_dict, messages=default_dict, **kwargs):
        if labels is not default_dict:
            kwargs['labels'] = labels
        if help_texts is not default_dict:
            kwargs['help_texts'] = help_texts
        if name is not default_str:
            kwargs['name'] = name
        if name_plural is not default_str:
            kwargs['name_plural'] = name_plural
        if errors is not default_dict:
            kwargs['errors'] = errors
        if messages is not default_dict:
            kwargs['messages'] = messages
        super(ModelTranslations, self).__init__(**kwargs)

    def inject(self, model_class):
        """Injects translations into the model class.

        Can be used as a decorator for your model.

        :param model_class: model class to inject with translations
        :return: the model class
        """
        apply_to_model(model_class, mapping=self)
        return model_class

    @property
    def help_texts(self):
        return self.subdict('help_texts')
