#!/usr/bin/env python
# encoding: utf-8

import os
import ConfigParser

from utils.common_utils import Dict


MYSQL_CONFIG = Dict(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='1234',
    database='test'
)

REDIS_CONFIG = Dict(
    host='127.0.0.1',
    port=6379,
    password='1234',
    db=0
)


MONGO_CONFIG = Dict(
    host="127.0.0.1",
    port=27017,
)

Celery = Dict(
    pidfile='~/data/celery/%n.pid',
    logfile='~/data/celery/%n%I.log'
)

LOG_DIR = '~/server_logs'

logging_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.cfg')
LOG_CONFIG = ConfigParser.ConfigParser(None)
LOG_CONFIG.read(logging_config_file_path)

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
