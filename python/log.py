#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import logging.handlers


# The terminal has 8 colors with codes from 0 to 7
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

# The background is set with 40 plus the number of the color,
# and the foreground with 30
COLORS = {
    'WARNING':  COLOR_SEQ % (30 + YELLOW) + 'WARNING' + RESET_SEQ,
    'INFO':     COLOR_SEQ % (30 + BLUE) + 'INFO' + RESET_SEQ,
    'DEBUG':    COLOR_SEQ % (30 + WHITE) + 'DEBUG' + RESET_SEQ,
    'CRITICAL': COLOR_SEQ % (30 + YELLOW) + 'CRITICAL' + RESET_SEQ,
    'ERROR':    COLOR_SEQ % (30 + RED) + 'ERROR' + RESET_SEQ,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg, "%X")
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            record.levelname = COLORS.get(record.levelname, record.levelname)
        return logging.Formatter.format(self, record)


class LoggingConfiguration(object):
    COLOR_FORMAT = "[" + BOLD_SEQ + "%(asctime)s" + RESET_SEQ + \
                   "][%(levelname)s] %(message)s"
    NO_COLOR_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s "
    FILE_FORMAT = '[%(asctime)s][%(levelname)-8s]' \
                  ' %(message)s' \
                  ' (%(filename)s:%(lineno)d)'

    @classmethod
    def set(cls, log_level, log_filename='/tmp/qdk2.log', append=False):
        """ Configure a rotating file logging
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Log to sys.stderr using log level passed through command line
        if log_level != logging.NOTSET:
            log_handler = logging.StreamHandler(sys.stdout)
            if sys.platform.find('linux') >= 0:
                formatter = ColoredFormatter(cls.COLOR_FORMAT)
            else:
                formatter = ColoredFormatter(cls.NO_COLOR_FORMAT, False)
            log_handler.setFormatter(formatter)
            log_handler.setLevel(log_level)
            logger.addHandler(log_handler)

        # Log to rotating file using DEBUG log level
        log_handler = logging.handlers.RotatingFileHandler(log_filename,
                                                           mode='a+',
                                                           backupCount=3)
        formatter = logging.Formatter(cls.FILE_FORMAT)
        log_handler.setFormatter(formatter)
        log_handler.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)

        if not append:
            # Create a new log file on every new
            # (i.e. not scheduled) invocation
            log_handler.doRollover()


info = logging.info
debug = logging.debug
warning = logging.warning
error = logging.error


def trace(f):
    def my_f(*args, **kwargs):
        debug("T> " + f.__name__)
        result = f(*args, **kwargs)
        debug("T< " + f.__name__)
        return result
    my_f.__name = f.__name__
    my_f.__doc__ = f.__doc__
    return my_f
