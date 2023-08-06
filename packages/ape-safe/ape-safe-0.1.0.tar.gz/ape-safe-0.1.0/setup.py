# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ape_safe']
install_requires = \
['eth-brownie>=1.13.2,<2.0.0', 'gnosis-py>=2.7.14,<3.0.0']

setup_kwargs = {
    'name': 'ape-safe',
    'version': '0.1.0',
    'description': 'Build complex Gnosis Safe transactions and safely preview them in a forked environment.',
    'long_description': None,
    'author': 'banteg',
    'author_email': 'banteeg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
