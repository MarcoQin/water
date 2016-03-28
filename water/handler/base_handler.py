#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        pass

    def get(self):
        pass

    @asynchronous
    @gen.coroutine
    def post(self):
        pass
