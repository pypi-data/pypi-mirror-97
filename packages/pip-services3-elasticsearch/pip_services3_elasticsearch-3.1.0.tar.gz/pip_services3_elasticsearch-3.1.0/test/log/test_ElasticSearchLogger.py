# -*- coding: utf-8 -*-
import os

from pip_services3_commons.config import ConfigParams

from pip_services3_elasticsearch.log.ElasticSearchLogger import ElasticSearchLogger
from test.fixtures.LoggerFixture import LoggerFixture


class TestElasticSearchLogger:
    __logger: ElasticSearchLogger
    __fixture: LoggerFixture

    @classmethod
    def setup_class(cls):
        host = os.environ.get('ELASTICSEARCH_SERVICE_HOST') or 'localhost'
        port = os.environ.get('ELASTICSEARCH_SERVICE_PORT') or 9200
        date_format = 'YYYYMMDD'

        cls.__logger = ElasticSearchLogger()
        cls.__fixture = LoggerFixture(cls.__logger)

        config = ConfigParams.from_tuples(
            'source', 'test',
            'index', 'log',
            'daily', True,
            "date_format", date_format,
            'connection.host', host,
            'connection.port', port
        )
        cls.__logger.configure(config)

        cls.__logger.open(None)

    @classmethod
    def teardown_class(cls):
        cls.__logger.close(None)

    def test_log_level(self):
        self.__fixture.test_log_level()

    def test_simple_logging(self):
        self.__fixture.test_simple_logging()

    def test_error_logging(self):
        self.__fixture.test_error_logging()

    def test_date_pattern_testing_1(self):
        """
        We test to ensure that the date pattern does not effect the opening of the elasticsearch component
        """
        host = os.environ.get('ELASTICSEARCH_SERVICE_HOST') or 'localhost'
        port = os.environ.get('ELASTICSEARCH_SERVICE_PORT') or 9200

        logger = ElasticSearchLogger()
        date_format = 'YYYY.MM.DD'

        config = ConfigParams.from_tuples(
            'source', 'test',
            'index', 'log',
            'daily', True,
            "date_format", date_format,
            'connection.host', host,
            'connection.port', port
        )
        logger.configure(config)
        logger.open(None)

        # Since the current_index property is private, we will just check for an open connection
        assert logger.is_open() is True

        logger.close(None)

    def test_date_pattern_testing_2(self):
        """
        We test to ensure that the date pattern does not effect the opening of the elasticsearch component
        """
        host = os.environ.get('ELASTICSEARCH_SERVICE_HOST') or 'localhost'
        port = os.environ.get('ELASTICSEARCH_SERVICE_PORT') or 9200

        logger = ElasticSearchLogger()
        date_format = 'YYYY.M.DD'

        config = ConfigParams.from_tuples(
            'source', 'test',
            'index', 'log',
            'daily', True,
            "date_format", date_format,
            'connection.host', host,
            'connection.port', port
        )
        logger.configure(config)
        logger.open(None)
        # Since the current_index property is private, we will just check for an open connection
        assert logger.is_open() is True
        logger.close(None)
