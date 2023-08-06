# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybloxy', 'pybloxy.classes']

package_data = \
{'': ['*']}

install_requires = \
['api>=0.0.7,<0.0.8']

setup_kwargs = {
    'name': 'pybloxy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'repl.it user',
    'author_email': 'replituser@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
