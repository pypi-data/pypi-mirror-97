# Provides addition properties for Azure Monitor under Azure Functions

This library is a sample of how to add additional properties that are queryable from Azure Monitor via traces.

## Goal

The purpose is to provide a simple way to query on the message title with some set prefix, the using the returned records apply addition query logic.

This library is coupled to [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python) package in addition to [OpenCensus](https://opencensus.io/exporters/supported-exporters/go/applicationinsights/).


### OpenCensus
More details are explained at [Set up Azure Monitor for your Python application](https://docs.microsoft.com/en-us/azure/azure-monitor/app/opencensus-python#instrument-with-opencensus-python-sdk-for-azure-monitor)

## Usage

### Installation

The package is published to [Pypi.org](https://pypi.org/project/azfunctionsmonitor/) and can be installed using normal `pip` or other Python package management tools.

```bash
pip install azfunctionsmonitor
```


Very simply you just ensure that the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable is set for the application such as in WebApps or Azure Functions.

Again refer to [OpenCensus](#opencensus) above for more.

```python
from azfunctionsmonitor import get_logger

logger = get_logger("my stuff") # LoggingHelper("zipper", logging.getLogger())
logger.info("hellow")
logger.debug("same same")
print("done")

```

If you don't have the OpenCensus `APPLICATIONINSIGHTS_CONNECTION_STRING` variable or it is set incorrectly:

```text
ERROR:root:failed to load opencensus AzureLogHandler: Instrumentation key cannot be none or empty.
Traceback (most recent call last):
  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/azfunctionsmonitor/LoggingHelper.py", line 61, in get_logger
    azure_handler = AzureLogHandler()
  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/opencensus/ext/azure/log_exporter/__init__.py", line 45, in __init__
    utils.validate_instrumentation_key(self.options.instrumentation_key)
  File "/Users/cicorias/g/cse/py/az-mon-test/.venv/lib/python3.7/site-packages/opencensus/ext/azure/common/utils.py", line 76, in validate_instrumentation_key
    raise ValueError("Instrumentation key cannot be none or empty.")
ValueError: Instrumentation key cannot be none or empty.
WARNING:root:[my stuff] logging set to WARNING
```