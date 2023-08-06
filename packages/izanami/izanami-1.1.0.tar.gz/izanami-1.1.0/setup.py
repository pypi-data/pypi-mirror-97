# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izanami']

package_data = \
{'': ['*'],
 'izanami': ['static/*',
             'static/highlight/*',
             'templates/*',
             'templates/action/*',
             'templates/hook/*',
             'templates/merge/*',
             'templates/repo/*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'docker>=4.4.4,<5.0.0',
 'fabric>=2.6.0,<3.0.0',
 'invoke>=1.5.0,<2.0.0',
 'mitama>=4.3.3,<5.0.0',
 'unidiff>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'izanami',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'boke0',
    'author_email': 'speken00.tt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
