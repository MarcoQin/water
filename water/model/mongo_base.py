#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient

from water.config import config

__connection_uri = "mongodb://{host}:{port}/".format(**config.MONGO_CONFIG)

__client = MongoClient(__connection_uri)

_raven_db = __client.raven


def get_db():
    return _raven_db
