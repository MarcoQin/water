#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        super(MainHandler, self).__init__(*request, **kwargs)

    def prepare(self):
        """
        Called at the beginning of a request before 'get' / 'post'/ etc.
        Here to process prepare extensions(or something like middleware).
        """
        pass

    def on_finish(self):
        """Called after the end of a request.
        Here to process clean extensions(or some other middleware).
        """

    def get(self):
        print self.request.path
        self.write("hello world")
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self):
        pass
