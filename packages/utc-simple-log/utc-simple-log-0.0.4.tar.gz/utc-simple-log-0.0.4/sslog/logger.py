"""
Simple log

More
https://github.com/ppd0523/utc-simple-log.git
"""

__all__ = ['SimpleLogger']

import logging.handlers
import os
import datetime as dt
import logging
import pytz
import time


class _KSTFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def converter(self, timestamp):
        ts = dt.datetime.fromtimestamp(timestamp)

        # KST datetime format 'Asia/Seoul'
        tz_info = pytz.timezone('Asia/Seoul')
        return tz_info.localize(ts)

    def formatTime(self, record, datefmt=None):
        formatter = self.converter(record.created)
        if datefmt:
            s = formatter.strftime(datefmt)
        else:
            try:
                s = formatter.isoformat(timespec='milliseconds')
            except TypeError:
                s = formatter.isoformat()
        return s


class _UTCFormatter(logging.Formatter):
    converter = time.gmtime


class _Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.__initialized = False
        return cls._instance


class SimpleLogger(_Singleton):
    __initialized = False

    def __init__(self, level=logging.DEBUG, *, formatter='UTC', file='./logs/log.txt', maxBytes=2000000, backupCount=5):
        """Logger
        :param level:
        SYMBOL              INTEGER
        logging.DEBUG       10
        logging.INFO        20
        logging.WARNING     30
        logging.ERROR       40
        logging.CRITICAL    50

        file: './logs/log.txt'
        maxBytes: 2,000,000 bytes
        backupCount : 5 files

        Example)
            logger = SimpleLogger()
            logger.setLevel(logging.INFO)
            logger.info('Hello world')
        """
        if self.__initialized: return
        self.__initialized = True

        self.__format_str = formatter

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.__getFormatter(formatter=formatter))

        abspath = os.path.abspath(file)
        _dir, _base = os.path.split(abspath)
        os.makedirs(_dir, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
                filename=abspath,  # log filename
                mode='a',               # append-mode (e.g. 'w' write-mode)
                maxBytes=maxBytes,       # 2MB
                backupCount=backupCount)          # max number of backup files
        file_handler.setFormatter(self.__getFormatter(formatter=formatter))

        self.__logger = logging.getLogger('Simple logger')
        self.__logger.setLevel(level=level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    @property
    def debug(self):
        return self.__logger.debug

    @property
    def info(self):
        return self.__logger.info

    @property
    def warning(self):
        return self.__logger.warning

    @property
    def error(self):
        return self.__logger.error

    @property
    def critical(self):
        return self.__logger.critical

    @property
    def fatal(self):
        return self.__logger.fatal

    def setLevel(self, level):
        """
        logging.DEBUG
        logging.INFO
        logging.WARN
        logging.ERROR
        logging.CRITICAL
        """
        self.__logger.setLevel(level=level)

    def setFormatter(self, format_str):
        """'KST' or 'UTC'"""
        self.__format_str = format_str
        self.__logger.handlers[0].formatter = self.__getFormatter(format_str)
        self.__logger.handlers[1].formatter = self.__getFormatter(format_str)

    def __getFormatter(self, formatter='UTC'):
        fmt = '%(asctime)s, [%(levelname)8s] [%(filename)s:%(funcName)s,L:%(lineno)d]: %(message)s'
        datefmt = '%Y-%m-%dT%H:%M:%S'

        if formatter == 'UTC':
            return _UTCFormatter(fmt=fmt, datefmt=datefmt)
        elif formatter == 'KST':
            return _UTCFormatter(fmt=fmt, datefmt=datefmt + '%z')
        elif formatter == 'Asia/Seoul':
            return _KSTFormatter(fmt=fmt, datefmt=datefmt)

    def _tests(self):
        self.__logger.debug('Debugging message')
        self.__logger.info('Info message')
        self.__logger.warning('Warning message')
        self.__logger.error('Error message')
        self.__logger.critical('Critical message')
        self.__logger.fatal('fatal message')


if __name__ == '__main__':
    logger = SimpleLogger()
    logger.setLevel(logging.DEBUG)
    logger._tests()