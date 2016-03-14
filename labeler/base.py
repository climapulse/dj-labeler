# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import


# Sentinel values -- different ones for dict and str to prevent IDEs from complaining about type differences.
default_dict = {}
default_str = ''


def resolve_dict_value(dictionary, path):
    """Allows fetching a values within nested dicts using a dot-delimited path.

    >>> my_dict = {'a': {'b': 'c': 1}}
    >>> assert resolve_dict_value(my_dict, 'a.b.c') == 1
    >>> assert resolve_dict_value(my_dict, 'a.b.c.d') is None

    :param dictionary: the dictionary
    :param path: path to resolve
    :return: the corresponding value or None
    """
    d = dictionary
    for key in path.split('.'):
        d = d.get(key)
        if d is None:
            return None
    return d


class Translations(dict):
    """Base class for translations.

    Instead of using a regular dict, we provide a subtype with some useful methods.

    """

    def subdict(self, key):
        """Fetches the dictionary identified by key.

        :param key: key for the dictionary value
        :return: the dictionary or an empty one
        """
        return self.get(key, {})

    def resolve(self, path):
        """Resolves a value using a dotted path.

        Uses ``resolve_dict_value``.
        """
        return resolve_dict_value(self, path)

    @property
    def labels(self):
        """Fetches the nested dictionary ``labels``."""
        return self.subdict('labels')

    @property
    def errors(self):
        """Fetches the nested dictionary ``errors``."""
        return self.subdict('errors')

    @property
    def error_messages(self):
        """Fetches the nested dictionary ``error_messages``."""
        return self.subdict('error_messages')

    @property
    def messages(self):
        """Fetches the nested dictionary ``messages``."""
        return self.subdict('messages')

