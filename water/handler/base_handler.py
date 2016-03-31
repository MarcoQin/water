#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, asynchronous
from tornado import gen

from extension.prepare_ext import FindView, EvalHandlerViewExt
from utils.exception_utils import NormalException
from utils.template_utils import AutoTemplate


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
        EvalHandlerViewExt(self)(prepare=True)  # find current view's extensions and evaluate

    def on_finish(self):
        """Called after the end of a request.
        Here to process clean up extensions(or some other middleware).
        """
        EvalHandlerViewExt(self)(prepare=False)  # find current view's extensions and evaluate

    @asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        status = 404
        error = False
        res = None
        if self.view:
            try:
                template = None
                kwargs = {}
                data = yield self.view(self).get(*self.path_args, **self.path_kwargs)
                if data:
                    if isinstance(data, (tuple, list)):
                        kwargs = data[1]
                        data = data[0]
                    if isinstance(data, AutoTemplate):
                        template = data.get_template()
                    else:
                        template = data
                    res = self.render_string(template, **kwargs)
            except NormalException as e:
                print e.message
                pass
            except Exception:
                self.tracker.trace_error()
                error = True
                status = 500
        else:
            error = True

        if error:
            self.send_error(status)
        else:
            if res:
                self.write(res)
        if not self._finished:
            self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        pass
