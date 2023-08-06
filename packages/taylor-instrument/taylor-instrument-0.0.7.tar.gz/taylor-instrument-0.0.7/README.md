# taylor-instrument service

### A service based on [Pip.Services toolkit](https://www.pipservices.org/docs/api/overview) that collect logs and metrics by Elasticsearch and Prometheus.

<a name="links"></a> Quick links:

* [pip-services3-commons](https://github.com/pip-services3-python/pip-services3-commons-python)
* [pip-services3-components](https://github.com/pip-services3-python/pip-services3-components-python)
* [pip-services3-rpc](https://github.com/pip-services3-python/pip-services3-rpc-python)
* [pip-services3-prometheus](https://github.com/pip-services3-python/pip-services3-prometheus-python)
* [pip-services3-elasticsearch](https://github.com/pip-services3-python/pip-services3-elasticsearch-python)

## Use

Install the Python package as
```bash
pip install taylor-instrument
```

Configure environment variables:

* INSTRUMENTATION_PORT - port number for instrument service (default: 8082)
* CORRELATION_ID - correlation id of the service
* ELASTICSEARCH_ENABLED - enable ElasticSearch logger
* ELASTICSEARCH_INFO - loge level (default: info)
* ELASTICSEARCH_SOURCE - source (context) name
* ELASTICSEARCH_PROTOCOL - connection protocol: http or https (default: http)
* ELASTICSEARCH_SERVICE_HOST - host name or IP address (default: localhost)
* ELASTICSEARCH_SERVICE_PORT - port number (default: 9200)
* PROMETHEUS_ENABLED - enable prometheus logs and metrics
* PROMETHEUS_PROTOCOL - connection protocol: http or https (default: http)
* PROMETHEUS_SERVICE_HOST - host name or IP address (default: localhost)
* PROMETHEUS_SERVICE_PORT - port number (default: 9090)
* PUSHGATEWAY_PROTOCOL - connection protocol: http or https (default: http)
* PUSHGATEWAY_METRICS_SERVICE_HOST - host name or IP address (default: localhost)
* PUSHGATEWAY_METRICS_SERVICE_PORT - port number (default: 9091)

For more environment configs see above links.

Then use loggers and metrics in your services:

```python
from pip_services3_commons.errors import ApplicationException
from pip_services3_components.log import LogLevel

from taylor_instrument import instrument, logger, counters
# Configure instrument
from taylor_instrument.metrics import metrics

instrument.set_correlation_id_from_file('./component.json')
instrument.logger.set_level(LogLevel.Debug)


def info_service():
    counters.increment_one('my_service.info.calls')
    timing = counters.begin_timing('my_service.info.exec_time')

    logger.warn(message='warning', correlation_id='my custom correlation id')
    logger.debug('debug')
    logger.trace('Trace')
    logger.error(ApplicationException(FileNotFoundError('My exception1')), 'my error message')
    logger.info('my custom correlation id', None, 'Info')
    logger.fatal(ApplicationException(IOError('My exception2')), 'Fatal exception')

    timing.end_timing()


@metrics('my-custom-optional-name')
def info_service_2():
    logger.info('Using decorator metrics %s', 'Info')


info_service()
info_service_2()

```

The loggers have next signatures:

```python
def log(self, level, error, message, *args, correlation_id=None, **kwargs):

def fatal(self, error, message, *args, correlation_id=None, **kwargs):

def error(self, error, message, *args, correlation_id=None, **kwargs):

def warn(self, message, *args, correlation_id=None, **kwargs):

def info(self, message, *args, correlation_id=None, **kwargs):

def debug(self, message,  *args, correlation_id=None, **kwargs):

def trace(self, message, *args, correlation_id=None, **kwargs):
```
See ```CustomCompositeLogger```
