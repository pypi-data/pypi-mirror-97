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
    'version': '0.1.111',
    'description': 'Loging helper for Azure Monitor and Open Census',
    'long_description': '# Provides addition properties for Azure Monitor under Azure Functions\n\nThis library is a sample of how to add additional properties that are queryable from Azure Monitor via traces.\n\n## Goal\n\nThe purpose is to provide a simple way to query on the message title with some set prefix, the using the returned records apply addition query logic.\n\nThis library is coupled to [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python) package in addition to [OpenCensus](https://opencensus.io/exporters/supported-exporters/go/applicationinsights/).\n\n\n### OpenCensus\nMore details are explained at [Set up Azure Monitor for your Python application](https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python#instrument-with-opencensus-python-sdk-for-azure-monitor)\n\n## Usage\n\n### Installation\n\nThe package is published to [Pypi.org](https://pypi.org/project/azfunctionsmonitor/) and can be installed using normal `pip` or other Python package management tools.\n\n```bash\npip install azfunctionsmonitor\n```\n\nVery simply you just ensure that the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable is set for the application such as in WebApps or Azure Functions.\n\nAgain refer to [OpenCensus](#opencensus) above for more.\n\n```python\nfrom azfunctionsmonitor import get_logger\n\nlogger = get_logger("my stuff") # LoggingHelper("zipper", logging.getLogger())\nlogger.info("hellow")\nlogger.debug("same same")\nprint("done")\n\n```\n\nIf you don\'t have the OpenCensus `APPLICATIONINSIGHTS_CONNECTION_STRING` variable or it is set incorrectly:\n\n```text\nERROR:root:failed to load opencensus AzureLogHandler: Instrumentation key cannot be none or empty.\nTraceback (most recent call last):\n  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/azfunctionsmonitor/LoggingHelper.py", line 61, in get_logger\n    azure_handler = AzureLogHandler()\n  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/opencensus/ext/azure/log_exporter/__init__.py", line 45, in __init__\n    utils.validate_instrumentation_key(self.options.instrumentation_key)\n  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/opencensus/ext/azure/common/utils.py", line 76, in validate_instrumentation_key\n    raise ValueError("Instrumentation key cannot be none or empty.")\nValueError: Instrumentation key cannot be none or empty.\nWARNING:root:[my stuff] logging set to WARNING\n```\n\n## Environment settings\n\nThere are essentially only two key environment varaibles that the library is directly aware of\n\n- `APPLICATIONINSIGHTS_CONNECTION_STRING` - which is what OpenCensus relies on\n- `LOGLEVEL` - this is equivalent to the Python log levels and can be set to `DEBUG`, `INFO`, `WARNING`, `ERROR` etc.',
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
