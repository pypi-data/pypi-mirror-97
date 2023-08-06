# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metroid',
 'metroid.management',
 'metroid.management.commands',
 'metroid.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.1,<4.0.0',
 'azure-servicebus>=7.0.1,<8.0.0',
 'celery>=5.0.0,<6.0.0',
 'django-guid>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'metroid',
    'version': '1.0.0',
    'description': 'Metroid - Metro for Django',
    'long_description': None,
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas.svensson@intility.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
