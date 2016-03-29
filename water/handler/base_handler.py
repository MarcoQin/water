#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen

from extension.prepare_ext import FindView, EvalHandlerView


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        super(MainHandler, self).__init__(*request, **kwargs)
        self.view = None

    def prepare(self):
        """
        Called at the beginning of a request before 'get' / 'post'/ etc.
        Here to process prepare extensions(or something like middleware).
        """
        FindView(self)()  # find process view via current visited url path
        EvalHandlerView(self)()  # find current view's extensions and evaluate

    def on_finish(self):
        """Called after the end of a request.
        Here to process clean up extensions(or some other middleware).
        """
        pass

    def get(self):
        if self.view:
            res = self.view(self).get()
            self.write(res)
            self.finish()
        self.send_error(404)
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self):
        pass
