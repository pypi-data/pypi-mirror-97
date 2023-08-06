# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybloxy', 'pybloxy.classes']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.2,<3.0']

setup_kwargs = {
    'name': 'pybloxy',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'R0bl0x10501050',
    'author_email': 'r0bl0x10501050@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
