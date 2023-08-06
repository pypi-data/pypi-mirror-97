# -*- coding: utf-8 -*-

import concurrent.futures
import json
import os

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor, Referencer
from pip_services3_commons.run import Opener, Closer
from pip_services3_components.count import LogCounters, CompositeCounters
from pip_services3_components.info import ContextInfo
from pip_services3_components.log import ConsoleLogger, LogLevel
from pip_services3_elasticsearch.log.ElasticSearchLogger import ElasticSearchLogger
from pip_services3_prometheus.count.PrometheusCounters import PrometheusCounters
from pip_services3_prometheus.services.PrometheusMetricsService import PrometheusMetricsService
from pip_services3_rpc.services import HttpEndpoint, HeartbeatRestService

from taylor_instrument.CustomCompositeLogger import CustomCompositeLogger


class Instrument:
    __future = None
    _correlation_id = None

    def __init__(self, service_name='', service_description=''):
        """
        Default context info does sets from correlation_id

        :param service_name: service name
        :param service_description: text description service
        """
        self._references: References
        self.service_name = service_name
        self.service_description = service_description

        self._context_info = ContextInfo(service_name, service_description)
        self._console_logger = ConsoleLogger()
        self._elasticsearch_logger = ElasticSearchLogger() if os.environ.get('ELASTICSEARCH_ENABLED') else None
        self._log_counters = LogCounters()
        self._prometheus_counters = PrometheusCounters() if os.environ.get('PROMETHEUS_ENABLED') else None

        self._http_endpoint = HttpEndpoint()
        self._prometheus_service = PrometheusMetricsService() if os.environ.get('PROMETHEUS_ENABLED') else None
        self._heartbeat_service = HeartbeatRestService()

        self.logger = CustomCompositeLogger()
        self.counters = CompositeCounters()

        self._configure()
        self._set_references()
        # self._decorate_loggers()

    def set_context(self, service_name, service_description):
        """
        Set context name and text description for container

        :param service_name: name of service
        :param service_description: service description
        """
        self._context_info.name = service_name
        self._context_info.description = service_description

    def _configure(self):
        self._console_logger.configure(ConfigParams.from_tuples(
            'level', os.environ.get('LOGGER_LEVEL', 'trace'),
            'source', os.environ.get('LOGGER_SOURCE')
        ))

        self.logger.configure(ConfigParams.from_tuples(
            'correlation_id', os.environ.get('CORRELATION_ID')))

        if self._elasticsearch_logger:
            self._elasticsearch_logger.configure(ConfigParams.from_tuples(
                'level', os.environ.get('ELASTICSEARCH_INFO', 'info'),
                'source', os.environ.get('ELASTICSEARCH_SOURCE'),

                'connection.protocol', os.environ.get('ELASTICSEARCH_PROTOCOL', 'http'),
                'connection.host', os.environ.get('ELASTICSEARCH_SERVICE_HOST', 'localhost'),
                'connection.port', os.environ.get('ELASTICSEARCH_SERVICE_PORT', 9200),

                'index', os.environ.get('ELASTICSEARCH_INDEX', 'log'),
                'daily', os.environ.get('ELASTICSEARCH_DAILY', True),
                'interval', os.environ.get('ELASTICSEARCH_INTERVAL', '10'),
                'max_cache_size', os.environ.get('ELASTICSEARCH_MAX_CACHE_SIZE', '100'),
                'reconnect', os.environ.get('ELASTICSEARCH_RECONNECT', '60'),
                'timeout', os.environ.get('ELASTICSEARCH_TIMEOUT', '30'),
                'date_format', os.environ.get('ELASTICSEARCH_DATE_FORMAT', 'YYYYMMDD'),
                'max_retries', os.environ.get('ELASTICSEARCH_MAX_RETRIES', '3'),
                'index_message', os.environ.get('ELASTICSEARCH_INDEX_MESSAGE', False),

            ))
        if self._prometheus_service and self._prometheus_counters:
            self._prometheus_counters.configure(ConfigParams.from_tuples(
                'connection.protocol', os.environ.get('PUSHGATEWAY_PROTOCOL', 'http'),
                'connection.host', os.environ.get('PUSHGATEWAY_METRICS_SERVICE_HOST', 'localhost'),
                'connection.port', os.environ.get('PUSHGATEWAY_METRICS_SERVICE_PORT', '9091'),
                'retries', os.environ.get('PUSHGATEWAY_RETRIES', '3'),
                'connect_timeout', os.environ.get('PUSHGATEWAY_CONNECT_TIMEOUT', '10'),
                'timeout', os.environ.get('PUSHGATEWAY_INVOCATION_TIMEOUT', '10'),
            ))

            self._prometheus_service.configure(ConfigParams.from_tuples(
                'connection.protocol', os.environ.get('PROMETHEUS_PROTOCOL', 'http'),
                'connection.host', os.environ.get('PROMETHEUS_SERVICE_HOST', 'localhost'),
                'connection.port', os.environ.get('PROMETHEUS_SERVICE_PORT', '9090'),
                'route', 'metrics'
            ))

        self._http_endpoint.configure(ConfigParams.from_tuples(
            'connection.host', '0.0.0.0',
            'connection.port', os.environ.get('INSTRUMENTATION_PORT', '8082'),
        ))

        self._heartbeat_service.configure(ConfigParams.from_tuples(
            'route', 'ping'
        ))

    def _set_references(self):

        self._references = References.from_tuples(
            Descriptor('pip-services', 'context-info', 'default', 'default', '1.0'), self._context_info,
            Descriptor('pip-services', 'logger', 'console', 'default', '1.0'), self._console_logger,
            Descriptor('pip-services', 'counters', 'console', 'default', '1.0'), self._log_counters,
            Descriptor('pip-services', 'endpoint', 'http', 'default', '1.0'), self._http_endpoint,
            Descriptor('pip-services', 'heartbeat-service', 'rest', 'default', '1.0'), self._heartbeat_service
        )

        if self._elasticsearch_logger:
            self._references.put(Descriptor('pip-services', 'logger', 'elasticsearch', 'default', '1.0'),
                                 self._elasticsearch_logger)
        if self._prometheus_service and self._prometheus_counters:
            self._references.put(Descriptor('pip-services', 'counters', 'prometheus', 'default', '1.0'),
                                 self._prometheus_counters)
            self._references.put(Descriptor('pip-services', 'metrics-service', 'prometheus', 'default', '1.0'),
                                 self._prometheus_service, )

        self.logger.set_references(self._references)
        self.counters.set_references(self._references)

    # def _decorate_loggers(self):
    #     for method_name in self.logger.__dir__():
    #         logger_method = getattr(self.logger, method_name)
    #         if not method_name.startswith('_') and 'correlation_id' in inspect.getfullargspec(logger_method).args:
    #             setattr(self.logger, method_name, self.__decorator(logger_method))
    #
    # def __decorator(self, fun):
    #     def wrapper_func(*args, **kwargs):
    #         if len(args) > 0 and args[0] is None:
    #             args = list(args)
    #             args[0] = self._correlation_id
    #         elif kwargs.get('correlation_id') is None:
    #             kwargs['correlation_id'] = self._correlation_id
    #         return fun(*args, **kwargs)
    #
    #     # Wrapper function add something to the passed function and decorator
    #     # returns the wrapper function
    #
    #     return wrapper_func

    def start(self):
        """
        Starts http service for logging and metrics
        """
        executor = concurrent.futures.ThreadPoolExecutor()
        Referencer.set_references(self._references, self._references.get_all())
        self.__future = executor.submit(
            Opener.open, None, self._references.get_all())
        self.__future.add_done_callback(lambda _obj: self.start)
        self.logger.debug("-- instrument starts --")

    def stop(self):
        """
        Stops http service for logging and metrics
        """
        try:
            if self.__future.exception():
                raise self.__future.exception()
            if not self.__future.done():
                self.__future.set_result(
                    KeyboardInterrupt('Server is stopped!'))
        finally:
            Closer.close(None, self._references.get_all())
            Referencer.unset_references(self._references.get_all())
            self.logger.debug("-- instrument is stopped --")

    def set_correlation_id_from_file(self, path: str):
        """
        Set one correlation id for all loggers and counters from file
        :param path: string path to json file with attr **name**

        Example file:

        .. code-block:: json

            {
                "name": "my service name",
                "version": "1.0.0",
                "build": 0
                ...
            }
        """
        with open(path, 'r') as json_file:
            self._correlation_id = json.load(json_file)['name']
            self.set_context(self.get_correlation_id(), f"{self.get_correlation_id()} service")
            self.logger._correlation_id = self.get_correlation_id()

    def set_correlation_id(self, correlation_id: str):
        """
        Set one correlation id for all loggers and counters from string

        :param correlation_id: string path to json file with attr **name**
        """
        self._correlation_id = correlation_id
        self.set_context(self.get_correlation_id(), f"{self.get_correlation_id()} service")
        self.logger._correlation_id = self.get_correlation_id()

    def get_correlation_id(self):
        """
        Return correlation_id of loggers and metrics

        :return: correlation id
        """
        return self._correlation_id


# Define logs and counters
instrument = Instrument('taylor-instrument', 'Instrument service of loggers and counters')
instrument.logger.set_level(LogLevel.Info)
instrument.start()

logger = instrument.logger
counters = instrument.counters
