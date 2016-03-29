#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen

from extension.prepare_ext import FindView, EvalHandlerView
from utils.exception_utils import NormalException


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        super(MainHandler, self).__init__(*request, **kwargs)
        self.view = None
        self.path_args = ()
        self.path_kwargs = {}
        self.tracker = self.application.tracker
        self.sys_logger = self.application.sys_logger

    def prepare(self):
        """
        Called at the beginning of a request before 'get' / 'post'/ etc.
        Here to process prepare extensions(or something like middleware).
        """
        FindView(self)()  # find process view via current visited url path
        EvalHandlerView(self)(prepare=True)  # find current view's extensions and evaluate

    def on_finish(self):
        """Called after the end of a request.
        Here to process clean up extensions(or some other middleware).
        """
        EvalHandlerView(self)(prepare=False)  # find current view's extensions and evaluate

    @asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        if self.view:
            try:
                data = yield self.view(self).get(*self.path_args, **self.path_kwargs)
                self.write(data)
                self.finish()
            except NormalException as e:
                print e.message
                pass
            except Exception as e:
                print e
                self.tracker.trace_error()
        self.send_error(404)
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        pass
