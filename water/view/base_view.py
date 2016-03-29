#!/usr/bin/env python
# encoding: utf-8

from tornado import gen


class BaseView(object):

    def __init__(self, *args, **kwargs):
        pass

    @property
    def extensions(self):
        return None

    @gen.coroutine
    def post(self):
        return None
