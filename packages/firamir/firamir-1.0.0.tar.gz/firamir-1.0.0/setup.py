# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['firamir']
setup_kwargs = {
    'name': 'firamir',
    'version': '1.0.0',
    'description': 'firamir.println("Text"), firamir.inputln("Text input")',
    'long_description': None,
    'author': 'TikOt Studio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
