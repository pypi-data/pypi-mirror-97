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
    'version': '1.0.1',
    'description': 'Metroid - Metro for Django',
    'long_description': '<p align="center"><h1 align=\'center\'>Metroid</h1></p>\n<p align="center">\n    <em>Subscribe, act, publish.</em>\n</p>\n<p align="center">\n    <a href="https://python.org">\n        <img src="https://img.shields.io/badge/python-v3.9+-blue.svg" alt="Python version">\n    </a>\n    <a href="https://djangoproject.com">\n        <img src="https://img.shields.io/badge/django-3.1.1+%20-blue.svg" alt="Django version">\n    </a>\n    <a href="https://docs.celeryproject.org/en/stable/">\n        <img src="https://img.shields.io/badge/celery-5.0.0+%20-blue.svg" alt="Celery version">\n    </a>\n    <a href="https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/servicebus/azure-servicebus">\n        <img src="https://img.shields.io/badge/azure--servicebus-7.0.1+%20-blue.svg" alt="ServiceBus version">\n    </a>\n    <a href="https://github.com/snok/django-guid/">\n        <img src="https://img.shields.io/badge/django--guid-3.2.0+-blue.svg" alt="Django GUID version">\n    </a>\n</p>\n<p align="center">\n    <a href="https://codecov.io/gh/intility/metroid">\n        <img src="https://codecov.io/gh/intility/metroid/branch/master/graph/badge.svg" alt="Codecov">\n    </a>\n    <a href="https://github.com/pre-commit/pre-commit">\n        <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="Pre-commit">\n    </a>\n    <a href="https://github.com/psf/black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">\n    </a>\n    <a href="http://mypy-lang.org">\n        <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="mypy">\n    </a>\n    <a href="https://pycqa.github.io/isort/">\n        <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="isort">\n    </a>\n</p>\n\n\n# Metroid - Metro for Django\n\nThis app is intended to streamline integration with Metro for all Django+Celery users by:\n\n* Asynchronous handling of subscriptions and messages with one command\n* Execute Celery tasks based on message topics, defined in `settings.py`\n* Retry failed tasks through your admin dashboard when using the `MetroidTask` base\n\n## Overview\n* `python` >= 3.9 - We\'re using the newest versions of type annotations\n* `django` >= 3.1.1 - For `asgiref`, settings\n* `celery` >= 5.0.0 - Execute tasks based on a subject\n* `django-guid` >= 3.2.0 - Storing correlation IDs for failed tasks in the database, making debugging easy\n\n\n### Implementation\n\nThe `python manage.py metroid` app is fully asynchronous, and has no blocking code. It utilizes `Celery` to execute tasks.\n\nIt works by:\n1. Going through all your configured subscriptions and start a new async connection for each one of them\n2. Metro sends messages on the subscriptions\n3. This app filters out messages matching subjects you have defined, and queues a celery task to execute\n   the function as specified for that subject  \n   3.1. If no task is found for that subject, the message is marked as complete\n4. The message is marked as complete after the Celery task has successfully been queued\n5. If the task is failed, an entry is automatically created in your database\n6. All failed tasks can be retried manually through the admin dashboard\n\n\n### Configure and install this package\n\n\n> **_Note_**\n> For a complete example, have a look in `demoproj/settings.py`.\n\n1. Create a `METROID` key in `settings.py` with all your subscriptions and handlers.\nExample settings:\n```python\nMETROID = {\n    \'subscriptions\': [\n        {\n            \'topic_name\': \'metro-demo\',\n            \'subscription_name\': \'sub-metrodemo-metrodemoerfett\',\n            \'connection_string\': config(\'CONNECTION_STRING_METRO_DEMO\', None),\n            \'handlers\': [\n               {\n                  \'subject\': \'MetroDemo/Type/GeekJokes\',\n                  \'regex\': False,\n                  \'handler_function\': \'demoproj.demoapp.services.my_func\'\n                }\n            ],\n        },\n    ]\n}\n```\n\nThe `handler_function` is defined by providing the full dotted path as a string. For example,`from demoproj.demoapp.services import my_func` is provided as `\'demoproj.demoapp.services.my_func\'`.\n\nThe handlers subject can be a regular expression or a string. If a regular expression is provided, the variable regex must be set to True. Example:\n ```python\n\'handlers\': [{\'subject\': r\'^MetroDemo/Type/.*$\',\'regex\':True,\'handler_function\': my_func}],\n ```\n\n\n\n2. Configure `Django-GUID`  by adding the app to your installed apps, to your middlewares and configuring logging\nas described [here](https://github.com/snok/django-guid#configuration).\nMake sure you enable the [`CeleryIntegration`](https://django-guid.readthedocs.io/en/latest/integrations.html#celery):\n```python\nfrom django_guid.integrations import CeleryIntegration\n\nDJANGO_GUID = {\n    \'INTEGRATIONS\': [\n        CeleryIntegration(\n            use_django_logging=True,\n            log_parent=True,\n        )\n    ],\n}\n```\n\n\n#### Creating your own handler functions\n\nYour functions will be called with keyword arguments for\n\n\n`message`, `topic_name`, `subscription_name` and `subject`. You function should in other words\nlook something like this:\n\n```python\ndef my_func(*, message: dict, topic_name: str, subscription_name: str, subject: str) -> None:\n```\n\n\n### Running the project\n1. Ensure you have redis running:\n```bash\ndocker-compose up\n```\n2. Run migrations\n```bash\npython manage.py migrate\n```\n3. Create an admin account\n```bash\npython manage.py createsuperuser\n```\n4. Start a worker:\n```python\ncelery -A demoproj worker -l info\n```\n5. Run the subscriber:\n```python\npython manage.py metroid\n```\n6. Send messages to Metro. Example code can be found in [`demoproj/demoapp/services.py`](demoproj/demoapp/services.py)\n7. Run the webserver:\n```python\npython manage.py runserver 8000\n```\n8. See failed messages under `http://localhost:8080/admin`\n\nTo contribute, please see [`CONTRIBUTING.md`](CONTRIBUTING.md)\n',
    'author': 'Jonas Krüger Svensson',
    'author_email': 'jonas.svensson@intility.no',
    'maintainer': 'Ali Arfan',
    'maintainer_email': 'ali.arfan@intility.no',
    'url': 'https://github.com/intility/metroid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
