#    Copyright 2021 SolarWinds, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" AppOptics APM agent-internal logging module.

The appoptics_apm internal logging is making use of the built-in Python logging module. The appoptics_apm package
creates a logging handler reporting to stderr where all log messages are reported to. All logging from appoptics_apm
can be stopped completely by invoking the disable_logger() method.

A log message has the following format:
    '<date> <time> [ <logger_name> <loggin_level> p#<process_id>.<thread_id>] <log_message>'

The logging level of the appoptics_apm logger can be configured with an integer in the range of -1 to 6, representing
the following severities:
    -1: logging disabled
     0: fatal messages
     1: errors
     2: warnings
     3: info
     4: debug low
     5: debug medium
     6: debug high

The log level should not be modified manually from outside the appoptics_apm package.

For package-internal purposes, the logging level can be configured by providing on of the above levels to the
`set_ao_log_level`. The setLevel method should not be used to modify logging levels of individual module logger
instances.

The name of the main logger is `appoptics_apm`. Each module should create its own child logger by simply calling
logging.getLogger(__name__) which will return a child logger of the `appoptics_apm` logger.
"""

import logging
import os


class AoLoggingLevel(object):
    """Abstract mapping class providing a conversion between appoptics_apm agent logging level and Python logging module
    logging levels.
    The appoptics_apm package has seven different log levels, which are defined in the debug_levels dictionary."""

    # maps string representation of appoptics_apm.ao_logging levels to their integer counterpart
    debug_levels = {
        'OBOE_DEBUG_DISABLE': -1,
        'OBOE_DEBUG_FATAL': 0,
        'OBOE_DEBUG_ERROR': 1,
        'OBOE_DEBUG_WARNING': 2,
        'OBOE_DEBUG_INFO': 3,
        'OBOE_DEBUG_LOW': 4,
        'OBOE_DEBUG_MEDIUM': 5,
        'OBOE_DEBUG_HIGH': 6,
    }

    # maps appoptics_apm log levels to python logging module log levels
    logging_map = {
        debug_levels['OBOE_DEBUG_DISABLE']: logging.CRITICAL,
        debug_levels['OBOE_DEBUG_FATAL']: logging.CRITICAL,
        debug_levels['OBOE_DEBUG_ERROR']: logging.ERROR,
        debug_levels['OBOE_DEBUG_WARNING']: logging.WARNING,
        debug_levels['OBOE_DEBUG_INFO']: logging.INFO,
        debug_levels['OBOE_DEBUG_LOW']: logging.DEBUG,
        debug_levels['OBOE_DEBUG_MEDIUM']: logging.DEBUG,
        debug_levels['OBOE_DEBUG_HIGH']: logging.DEBUG,
    }

    @classmethod
    def default_level(cls):
        """Returns integer representation of default debugging level"""
        return cls.debug_levels['OBOE_DEBUG_WARNING']

    @classmethod
    def is_valid_level(cls, level):
        """Returns True if the provided level is a valid interger representation of a appoptics_apm.ao_logging level,
        False otherwise."""
        try:
            level = int(level)
            return bool(level in list(cls.debug_levels.values()))
        except (ValueError, TypeError):
            return False


# NullHandler does not exists in Python 2, thus create one if necessary
if not (hasattr(logging, 'NullHandler') and callable(logging.NullHandler)):

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

    logging.NullHandler = NullHandler


def _create_stream_handler():
    """Creates stream handler reporting to stderr."""
    sh = logging.StreamHandler()  # get stream handler to custom logging prefix
    f = logging.Formatter('%(asctime)s [ %(name)s %(levelname)-8s p#%(process)d.%(thread)d] %(message)s')
    sh.setFormatter(f)
    return sh


_stream_handler = _create_stream_handler()


def _get_logger():
    """Creates the logger for agent-internal logging.
    By default, the logging level of the created logger will be set to AoLoggingLevel.default_level().
    If the logging level of the agent-internal logger needs to be changed, this should happen through one of the
    following options only:
    (1) Through environment variable APPOPTICS_DEBUG_LEVEL
        - When _get_logger is invoked, APPOPTICS_DEBUG_LEVEL is checked and the logging level will be set to the
          value provided by the variable. If an invalid value has been provided, the logging level will not be changed.
    (2) By invoking set_ao_log_level
    """

    # create base logger for appoptics_apm package
    _logger = logging.getLogger('appoptics_apm')

    # configure logging level of appoptics_apm logger
    log_level = AoLoggingLevel.default_level()
    # check if APPOPTICS_DEBUG_LEVEL has been set and configure newly created logger accordingly
    envv_val = os.getenv('APPOPTICS_DEBUG_LEVEL', None)
    if envv_val is not None:
        if not AoLoggingLevel.is_valid_level(envv_val):
            _logger.warning("Misconfigured APPOPTICS_DEBUG_LEVEL ignored. Defaulted to debug_level %s", log_level)
        else:
            log_level = int(envv_val)

    _logger.setLevel(AoLoggingLevel.logging_map[log_level])

    if log_level != AoLoggingLevel.debug_levels['OBOE_DEBUG_DISABLE']:
        _logger.addHandler(_stream_handler)
    else:
        _logger.propagate = False
        _logger.addHandler(logging.NullHandler())

    return _logger


logger = _get_logger()


def disable_logger(disable=True):
    """Disables all logging messages from the `appoptics_apm` package when disable is True.
    To restoring logging, set disable as False.
    """
    if disable:
        logger.addHandler(logging.NullHandler())
        logger.removeHandler(_stream_handler)
        logger.propagate = False
    else:
        logger.addHandler(_stream_handler)
        logger.removeHandler(logging.NullHandler())
        logger.propagate = True


def set_ao_log_level(level):
    """Set the logging level of the agent-internal logger to the provided level. This function expects the level
    to be one of the integer representations of the levels defined in AoLoggingLevel.debug_levels.
    If an invalid level has been provided, the logging level will not be changed but a warning message will be emitted.

    This function should not be used from outside the appoptics_apm package to modify agent logging behaviour.
    """
    if AoLoggingLevel.is_valid_level(level):
        logger.setLevel(AoLoggingLevel.logging_map[level])
        if level == AoLoggingLevel.debug_levels['OBOE_DEBUG_DISABLE']:
            disable_logger()
    else:
        logger.warning("set_ao_log_level: Ignore attempt to set appoptics_apm logger to invalid logging level.")
