# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from .base import resolve_dict_value, Translations
from .forms import FormTranslations, apply_to_form
from .models import ModelTranslations, apply_to_model


VERSION = (1, 1, 0)
__version__ = '.'.join(['%s' % s for s in VERSION])
