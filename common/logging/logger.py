import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class CustomizeLogger:
    LOGGER = None

    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        if not cls.LOGGER:
            cls.LOGGER = cls.customize_logging(
                os.path.join(logging_config.get('path'), logging_config.get('filename')),
                level='info',
                retention=logging_config.get('retention'),
                rotation=logging_config.get('rotation'),
                format=logging_config.get('format')
            )
        return cls()

    @classmethod
    def customize_logging(
            cls,
            filepath: str,
            level: str,
            rotation: str,
            retention: str,
            format: str
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config


class DittoAppLogger(CustomizeLogger):
    """"""

    @staticmethod
    def format_log_message(short_message: str = None, long_message: Any = None):
        """"""
        try:
            if short_message is None:
                short_message = ''
            if long_message is None:
                long_message = ''
            serialized = f"MESSAGE: {json.dumps(short_message)}| {json.dumps(long_message)}"
        except Exception as exp:
            print("ERROR_WHILE_LOGGING_FORMATTING", exp)
            return short_message
        else:
            return serialized

    @classmethod
    def debug(cls, short_message: str = None, long_message: Any = None):
        """"""
        try:
            message = cls.format_log_message(short_message, long_message)
            cls.LOGGER.debug(message)
        except Exception as exp:
            print("ERROR_WHILE_LOGGING", exp)

    @classmethod
    def info(cls, short_message: str = None, long_message: Any = None):
        """"""
        try:
            message = cls.format_log_message(short_message, long_message)
            cls.LOGGER.info(message)
        except Exception as exp:
            print("ERROR_WHILE_LOGGING", exp)

    @classmethod
    def warning(cls, short_message: str = None, long_message: Any = None):
        """"""
        try:
            message = cls.format_log_message(short_message, long_message)
            cls.LOGGER.warning(message)
        except Exception as exp:
            print("ERROR_WHILE_LOGGING", exp)

    @classmethod
    def error(cls, short_message: str = None, long_message: Any = None):
        """"""
        try:
            message = cls.format_log_message(short_message, long_message)
            cls.LOGGER.error(message)
        except Exception as exp:
            print("ERROR_WHILE_LOGGING", exp)

    @classmethod
    def exception(cls, short_message, exception: Exception):
        """"""
        try:
            cls.LOGGER.exception(short_message, exception)
        except Exception as exp:
            print("ERROR_WHILE_LOGGING", exp)
