# -*- coding: utf-8 -*-
import time

from pip_services3_components.log import LogLevel


class LoggerFixture:
    def __init__(self, logger):
        self.__logger = logger

    def test_log_level(self):
        assert self.__logger.get_level() >= LogLevel.Nothing
        assert self.__logger.get_level() <= LogLevel.Trace

    def test_simple_logging(self):
        self.__logger.set_level(LogLevel.Trace)

        self.__logger.fatal(None, None, 'Fatal error message')
        self.__logger.error(None, None, 'Error message')
        self.__logger.warn(None, 'Warning message')
        self.__logger.info(None, 'Information message')
        self.__logger.debug(None, 'Debug message')
        self.__logger.trace(None, 'Trace message')

        self.__logger.dump()
        time.sleep(1)

    def test_error_logging(self):
        try:
            # Raise an exception
            raise Exception('test')
        except Exception as err:
            self.__logger.fatal('123', err, 'Fatal error')
            self.__logger.error('123', err, 'Recoverable error')
            assert err is not None

        self.__logger.dump()
        time.sleep(1)