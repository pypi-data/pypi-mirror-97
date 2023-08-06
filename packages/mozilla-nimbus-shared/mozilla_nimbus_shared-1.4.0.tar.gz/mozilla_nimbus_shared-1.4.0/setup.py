# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozilla_nimbus_shared']

package_data = \
{'': ['*'],
 'mozilla_nimbus_shared': ['schemas/experiments/*',
                           'schemas/features/*',
                           'schemas/messaging/*',
                           'schemas/normandy/*',
                           'schemas/targeting/*',
                           'schemas/test/*']}

install_requires = \
['jsonschema>=3.2,<4.0']

setup_kwargs = {
    'name': 'mozilla-nimbus-shared',
    'version': '1.4.0',
    'description': 'Shared data and schemas for Project Nimbus',
    'long_description': '# Nimbus Shared ![CircleCI](https://img.shields.io/circleci/build/github/mozilla/nimbus-shared) ![npm (scoped)](https://img.shields.io/npm/v/@mozilla/nimbus-shared)\n\nThis is a place to define data and schemas used across Project Nimbus.\n\nAny data that moves between systems should have TypeScript types defined here, which will be\nautomatically converted to JSON Schema. Any data that needs to be re-used by multiple systems should\nbe stored here to be shared.\n\nFor more information on the data and schemas included here, how to use them, and how to add to them,\nsee the documentation at https://mozilla.github.io/nimbus-shared\n',
    'author': 'Michael Cooper',
    'author_email': 'mcooper@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
