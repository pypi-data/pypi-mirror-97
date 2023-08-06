# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['koumura']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.1']

setup_kwargs = {
    'name': 'koumura',
    'version': '0.2.1',
    'description': 'Functions for working with this data repository: https://figshare.com/articles/BirdsongRecognition/3470165',
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
