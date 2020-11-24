# _*_ coding:utf-8 _*_

from __future__ import absolute_import
import os
import logging
import logging.handlers
from . import config

_levelNames = {
    logging.CRITICAL: 'CRITICAL',
    logging.ERROR: 'ERROR',
    logging.WARNING: 'WARNING',
    logging.INFO: 'INFO',
    logging.DEBUG: 'DEBUG',
    logging.NOTSET: 'NOTSET',
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}
LOG_LEVELS = dict(_levelNames)
LOG_LEVELS.setdefault('FATAL', logging.FATAL)
LOG_LEVELS.setdefault(logging.FATAL, 'FATAL')
DISABLE_TRACEBACKS = os.environ.get('DISABLE_TRACEBACKS')


def init_log(log_path, **kwargs):
    """
    init_log - initialize log module
    Args:
        log_path      - Log file path prefix.
                              Log data will go to two files: log_path.log and log_path.log.wf
                              Any non-exist parent directories will be created automatically
        level         - msg above the level will be displayed
                              DEBUG < INFO < WARNING < ERROR < CRITICAL
        the default value is logging.INFO
        when          - how to split the log file by time interval
        'S' : Seconds
        'M' : Minutes
        'H' : Hours
        'D' : Days
        'W' : Week day
        default value: 'D'
            format        - format of the log
        default format:
            %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
            INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
        backup        - how many backup file to keep
        default value: 7
    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    level = kwargs.get('level', 'INFO')
    level = _levelNames.get(level)
    when = kwargs.get('when', 'D')
    backup = kwargs.get('backup', 7)
    log_format = kwargs.get(
        'log_format',
        '%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d - %(thread)d %(message)s'
    )
    date_fmt = kwargs.get('date_fmt', '%m-%d %H:%M:%S')
    formatter = logging.Formatter(log_format, date_fmt)
    logger = logging.getLogger()
    logger.setLevel(level)
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when=when,
        backupCount=backup
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.handlers.TimedRotatingFileHandler(
        log_path+".wf",
        when=when,
        backupCount=backup
    )
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger(category):
    log_file = os.path.join(config.LOG_DIR, '{0}.log'.format(category))
    if not os.path.exists(config.LOG_DIR):
        os.makedirs(config.LOG_DIR)
    level = config.LOG_VERBOSE if config.LOG_VERBOSE else 'DEBUG'
    init_log(log_path=log_file, level=level)

