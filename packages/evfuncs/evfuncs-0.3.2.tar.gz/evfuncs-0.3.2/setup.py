# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['evfuncs']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1', 'scipy>=1.2.0']

setup_kwargs = {
    'name': 'evfuncs',
    'version': '0.3.2',
    'description': 'Functions for working with files created by the EvTAF program and the evsonganaly GUI',
    'long_description': None,
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
