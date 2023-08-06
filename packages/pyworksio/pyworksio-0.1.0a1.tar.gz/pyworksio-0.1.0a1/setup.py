# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworksio', 'pyworksio.mailer']

package_data = \
{'': ['*']}

install_requires = \
['pyworks-mailer==0.0.1rc2']

setup_kwargs = {
    'name': 'pyworksio',
    'version': '0.1.0a1',
    'description': 'PyWorks is an open source framework for fast-up web production.',
    'long_description': None,
    'author': 'PyWorks Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
