#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        super(MainHandler, self).__init__(*request, **kwargs)

    def get(self):
        print self.request.path
        self.write("hello world")
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self):
        pass
