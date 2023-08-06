# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bridger',
 'bridger.buttons',
 'bridger.clubhouse',
 'bridger.display',
 'bridger.docs',
 'bridger.endpoints',
 'bridger.filters',
 'bridger.fsm',
 'bridger.history',
 'bridger.markdown',
 'bridger.menus',
 'bridger.metadata',
 'bridger.metadata.configs',
 'bridger.migrations',
 'bridger.notifications',
 'bridger.notifications.viewsets',
 'bridger.pandas',
 'bridger.preview',
 'bridger.search',
 'bridger.serializers',
 'bridger.serializers.fields',
 'bridger.share',
 'bridger.signals',
 'bridger.tags',
 'bridger.tests',
 'bridger.tests.selenium',
 'bridger.titles',
 'bridger.utils',
 'bridger.viewsets',
 'bridger.websockets']

package_data = \
{'': ['*'], 'bridger': ['templates/bridger/*', 'templates/bridger/admin/*']}

install_requires = \
['celery[redis]>=4.4.0,<4.5.0',
 'channels>=2.4.0,<2.5.0',
 'channels_redis[cryptography]>=3.0.0,<3.1.0',
 'django-celery-beat>=2.0.0,<2.1.0',
 'django-filter>=2.2.0,<2.3.0',
 'django-fsm>=2.7.0,<2.8.0',
 'django-rest-fuzzysearch>=0.5.1,<0.6.0',
 'django-simple-history>=2.11.0,<2.12.0',
 'django>=3.0.0,<3.1.0',
 'djangorestframework-simplejwt>=4.3.0,<4.4.0',
 'djangorestframework>=3.11.0,<3.12.0',
 'inscriptis>=1.1,<2.0',
 'jsonschema>=3.2.0,<3.3.0',
 'markdown-blockdiag>=0.7.0,<0.8.0',
 'markdown>=3.2.0,<3.3.0',
 'numpy>=1.19.0,<1.20.0',
 'pandas',
 'pillow>=7.2.0,<7.3.0',
 'plotly>=4.0.0,<5.0.0',
 'psycopg2-binary>=2.8.0,<2.9.0',
 'pytest-selenium>=1.17.0,<1.18.0',
 'python-decouple==3.3',
 'python-slugify',
 'requests>=2.24.0,<2.25.0',
 'selenium>=3.141.0,<3.142.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'django-bridger',
    'version': '0.10.35',
    'description': 'The bridge between a Django Backend and a Javascript based Frontend',
    'long_description': None,
    'author': 'Christopher Wittlinger',
    'author_email': 'c.wittlinger@intellineers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
