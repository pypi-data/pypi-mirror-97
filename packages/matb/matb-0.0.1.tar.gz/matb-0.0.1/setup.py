# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['matb']
setup_kwargs = {
    'name': 'matb',
    'version': '0.0.1',
    'description': 'Matb sdohla',
    'long_description': None,
    'author': 'Otchim tvoi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
