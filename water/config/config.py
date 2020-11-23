#!/usr/bin/env python
# encoding: utf-8

import os
import configparser

from water.utils.common_utils import Dict


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
    pidfile='/home/data/celery/%n.pid',
    logfile='/home/data/celery/%n%I.log'
)

LOG_DIR = './server_logs'

logging_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.cfg')
LOG_CONFIG = configparser.ConfigParser()
LOG_CONFIG.read(logging_config_file_path)

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1

SMTP_CONFIG = Dict(
    HOST='somehost.somedomain.com',
    USER='someuser@somedomain.com',
    PASSWORD='password',
    FROM='service@somedomain.com'
)
