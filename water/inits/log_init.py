#!/usr/bin/env python
# encoding: utf-8

import os
import logging
from logging import config as logging_config

from config.config import LOG_CONFIG, LOG_DIR


def __fileConfig(config, disable_existing_loggers=True):
    """
    Read the logging configuration from a ConfigParser-format file.

    This can be called several times from an application, allowing an end user
    the ability to select from various pre-canned configurations (if the
    developer provides a mechanism to present the choices and load the chosen
    configuration).
    """

    formatters = logging_config._create_formatters(config)

    # critical section
    logging._acquireLock()
    try:
        logging._handlers.clear()
        del logging._handlerList[:]
        # Handlers add themselves to logging._handlers
        handlers = logging_config._install_handlers(config, formatters)
        logging_config._install_loggers(config, handlers, disable_existing_loggers)
    finally:
        logging._releaseLock()


def init_log(port):

    # configParser-format file
    cpf = LOG_CONFIG

    # change logging handle's filename
    for item in ('handler_sys', 'handler_track'):
        args = list(eval(cpf.get(item, 'args').strip()))
        log_dir = os.path.join(LOG_DIR, os.path.dirname(args[0]))
        args[0] = os.path.join(LOG_DIR, '%s_%s'% (args[0], port))
        cpf.set(item, 'args', str(tuple(args)))
        # init log file dirs
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    __fileConfig(cpf)
