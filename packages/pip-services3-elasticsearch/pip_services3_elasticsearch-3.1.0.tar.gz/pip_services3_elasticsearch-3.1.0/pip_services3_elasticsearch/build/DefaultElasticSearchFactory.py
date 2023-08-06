# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from log.ElasticSearchLogger import ElasticSearchLogger


class DefaultElasticSearchFactory(Factory):
    """
    Creates ElasticSearch components by their descriptors.

    See :class:`ElasticSearchLogger <log.ElasticSearchLogger>`
    """
    descriptor = Descriptor("pip-services", "factory", "elasticsearch", "default", "1.0")
    elastic_search_logger_descriptor = Descriptor("pip-services", "logger", "elasticsearch", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(DefaultElasticSearchFactory, self).__init__()
        self.register_as_type(DefaultElasticSearchFactory.elastic_search_logger_descriptor, ElasticSearchLogger)
