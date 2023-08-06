# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaqi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyaqi',
    'version': '0.1.0',
    'description': 'Módulo para cálculo do Índice de Qualidade do Ar (IQAr).',
    'long_description': None,
    'author': 'Fernanda Scovino',
    'author_email': 'fscovinom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
