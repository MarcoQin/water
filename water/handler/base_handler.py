#!/usr/bin/env python
# encoding: utf-8

import json
from tornado.web import RequestHandler, asynchronous
from tornado import gen

from extension.prepare_ext import FindView, EvalHandlerViewExt
from extension.common_ext import PrepareParams, RequestLog, ResponseLog
from utils.exception_utils import NormalException
from utils.template_utils import AutoTemplate
from utils.web_utils import Redirect
from utils.common_utils import JsonEncoder
from constant.const_error import AutoError


class MainHandler(RequestHandler):

    def __init__(self, *request, **kwargs):
        super(MainHandler, self).__init__(*request, **kwargs)
        self.view = None
        self.path_args = ()
        self.path_kwargs = {}
        self.tracker = self.application.tracker
        self.sys_logger = self.application.sys_logger

        self.status = 404
        self.error = False
        self.res = None

        self.arguments = {}

    def prepare(self):
        """
        Called at the beginning of a request before 'get' / 'post'/ etc.
        Here to process prepare extensions(or something like middleware).
        """
        FindView(self)()  # find process view via current visited url path
        RequestLog(self)()

    def on_finish(self):
        """Called after the end of a request.
        Here to process clean up extensions(or some other middleware).
        """
        ResponseLog(self)()
        self._eval_custom_extension('finish')

    def _eval_custom_extension(self, node=None):
        """
        Process every moments' extensions

        @type node: basestring
        @param node: one of ('prepare', 'finish', 'param')
        @return: None or numbers of evaluated extensions.
        """
        if not node:
            return
        return EvalHandlerViewExt(self)(node)  # find current view's extensions and evaluate

    @asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        if self.view:
            try:
                # ###----Node: params' handle----####
                if not self._eval_custom_extension('param'):
                    PrepareParams(self)()
                # ###----End Node: params' handle----####
                template = None
                kwargs = {}
                data = yield self.view(self).get(*self.path_args, **self.path_kwargs)
                if data:
                    if isinstance(data, tuple):
                        kwargs = data[1]
                        data = data[0]
                    if isinstance(data, AutoTemplate):
                        template = data.get_template()
                    elif isinstance(data, Redirect):
                        data.do_redirect(self)
                        return
                    else:
                        template = data
                    self.res = self.render_string(template, **kwargs)
            except NormalException as e:
                template = AutoTemplate('static/error.html').get_template()
                self.res = self.render_string(template, message=e.message)
            except Exception:
                self.tracker.trace_error()
                self.error = True
                self.status = 500
        else:
            self.error = True

        if self.error:
            self.send_error(self.status)
        else:
            if self.res is not None:
                self.write(self.res)
        if not self._finished:
            self.finish()

    @asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        if self.view:
            try:
                # ###----Node: params' handle----####
                if not self._eval_custom_extension('param'):
                    PrepareParams(self)()
                # ###----End Node: params' handle----####
                data = yield self.view(self).post(*self.path_args, **self.path_kwargs)
                if data:
                    if isinstance(data, tuple):
                        data = data[0]
                self.res = data and data or {}
            except NormalException as e:
                self.res = AutoError(e.code, e.ext).build_errors()
            except Exception:
                self.tracker.trace_error()
                self.status = 500
                self.error = True
        else:
            self.error = True

        if self.error:
            self.send_error(self.status)
        else:
            if self.res is not None:
                self.res = self.build_res(self.res)
                self.write(self.res)
        if not self._finished:
            self.finish()

    def build_res(self, res):
        if not isinstance(res, basestring):
            res = json.dumps(res, cls=JsonEncoder)
        return res
