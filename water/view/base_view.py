#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from utils.common_utils import classproperty


class BaseView(object):

    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        self.tracker = handler.tracker
        self.logger = handler.tracker
        self.arguments = handler.arguments
        self.params = self.arguments

    @classproperty
    def extensions(cls):
        return None

    @gen.coroutine
    def get(self):
        return None

    @gen.coroutine
    def post(self):
        return None
