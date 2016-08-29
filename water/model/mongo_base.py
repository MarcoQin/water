#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient

from water.config import config

__connection_uri = "mongodb://{host}:{port}/".format(**config.MONGO_CONFIG)

__client = MongoClient(__connection_uri)

_db = __client.some_collection


def get_db():
    return _db
