# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knopfler']

package_data = \
{'': ['*'], 'knopfler': ['templates/*']}

install_requires = \
['sanic']

extras_require = \
{'matrix': ['matrix_client'], 'rocketchat': ['RocketChatAPIBot']}

entry_points = \
{'console_scripts': ['knopfler = knopfler.knopfler:main']}

setup_kwargs = {
    'name': 'knopfler',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Andreas Nüßlein',
    'author_email': 'andreas@nuessle.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
