# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texto']

package_data = \
{'': ['*']}

install_requires = \
['nltk>=3.5,<4.0', 'spacy>=3.0.3,<4.0.0']

entry_points = \
{'console_scripts': ['texto = entry:main']}

setup_kwargs = {
    'name': 'texto',
    'version': '0.1.0',
    'description': 'Projet de textométrie.',
    'long_description': None,
    'author': 'Jérémy DEMANGE',
    'author_email': 'jeremy@scrapfast.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
