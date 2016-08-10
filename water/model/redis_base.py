#!/usr/bin/env python
# encoding: utf-8

import redis

from water.config import config

__pool = redis.ConnectionPool(**config.REDIS_CONFIG)
_db = redis.Redis(connection_pool=__pool)


def get_db():
    return _db
