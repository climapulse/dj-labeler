# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import labeler
import os


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = labeler.__version__


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dj-labeler',
    version=version,
    description='A Django library to externalize translation strings from models and forms.',
    long_description=README,
    author='Climapulse NV',
    author_email='kevin.wetzels@climapulse.com',
    url='https://github.com/climapulse/dj-labeler',
    packages=[
        'labeler'
    ],
    include_package_data=True,
    install_requires=[
        'Django'
    ],
    license='BSD',
    keywords=['dj-labeler', 'django', 'i18n'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
