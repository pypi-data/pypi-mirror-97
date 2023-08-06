# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intent_markup']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['build = poetry_scripts:build',
                     'clean = poetry_scripts:clean',
                     'install = poetry_scripts:install',
                     'publish = poetry_scripts:publish',
                     'test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'intent-markup',
    'version': '0.6.0',
    'description': 'Intent Markup library for digital assistant of AIOS.',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': 'contact@leftshift.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
