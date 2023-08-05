# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['binteger']
setup_kwargs = {
    'name': 'binteger',
    'version': '0.7.0',
    'description': 'Binary INTeger representation toolkit',
    'long_description': None,
    'author': 'hellman',
    'author_email': 'hellman@affine.group',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
