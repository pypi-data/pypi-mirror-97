# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qset',
 'qset.utils',
 'qset.utils.builtin',
 'qset.utils.coder',
 'qset.utils.coder.coders',
 'qset.utils.coder.coders.json',
 'qset.utils.coder.coders.msgpack',
 'qset.utils.numeric',
 'qset.utils.pandas_writer',
 'qset.utils.split_file',
 'qset.utils.time',
 'qset.utils.tqdm']

package_data = \
{'': ['*']}

install_requires = \
['Delorean>=1.0.0,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'msgpack>=1.0.0,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'tenacity>=6.2.0,<7.0.0',
 'tqdm>=4.50.2,<5.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'qset-python-client',
    'version': '0.1.5',
    'description': 'Python client for Qset API',
    'long_description': None,
    'author': 'akadaner',
    'author_email': 'arseniikadaner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
