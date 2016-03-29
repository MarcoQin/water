#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from utils.common_utils import classproperty

class BaseView(object):

    def __init__(self, *args, **kwargs):
        pass

    @classproperty
    def extensions(cls):
        return None

    @gen.coroutine
    def get(self):
        return None

    @gen.coroutine
    def post(self):
        return None
