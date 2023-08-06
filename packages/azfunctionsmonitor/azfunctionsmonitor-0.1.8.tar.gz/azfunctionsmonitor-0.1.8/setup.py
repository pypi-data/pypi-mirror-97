# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azfunctionsmonitor']

package_data = \
{'': ['*']}

install_requires = \
['azure-functions>=1.6.0,<2.0.0', 'opencensus-ext-azure>=1.0.7,<2.0.0']

setup_kwargs = {
    'name': 'azfunctionsmonitor',
    'version': '0.1.8',
    'description': 'Loging helper for Azure Monitor and Open Census',
    'long_description': '# A library to help logging to Azure Montior\n',
    'author': 'Shawn Cicoria',
    'author_email': 'github@cicoria.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cicorias/az-monitor-py-logging-pkg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
