#!/usr/bin/env python
# encoding: utf-8

import json
from tornado.web import RequestHandler
from tornado import gen

from water.extension.prepare_ext import FindView, EvalHandlerViewExt
from water.extension.common_ext import PrepareParams, RequestLog, ResponseLog
from water.utils.exception_utils import NormalException
from water.utils.template_utils import AutoTemplate
from water.utils.web_utils import Redirect
from water.utils.common_utils import JsonEncoder
from water.constant.const_error import AutoError
# from water.model.mysql_base import get_session


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
        # ResponseLog(self)()
        self._eval_custom_extension('finish')
        #  release the mysql session
        # get_session().remove()

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

    @gen.coroutine
    def get(self, *args, **kwargs):
        if self.view:
            try:
                # ###----Node: params' handle----####
                PrepareParams(self)()
                self._eval_custom_extension('param')
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
                    elif isinstance(data, (str, bytes)):
                        template = data
                    else:
                        template = None
                    if template is not None:
                        self.res = self.render_string(template, **kwargs)
                    else:
                        self.set_header("Content-Type", "application/json")
                        self.res = self.build_res(data)
                else:
                    self.set_header("Content-Type", "application/json")
                    self.res = self.build_res(data)
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
            self._eval_custom_extension('res')
            if self.res is not None:
                self.write(self.res)
        if not self._finished:
            self.finish()

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        if self.view:
            try:
                # ###----Node: params' handle----####
                PrepareParams(self)()
                self._eval_custom_extension('param')
                self._eval_custom_extension('post_param')
                # ###----End Node: params' handle----####
                data = yield self.view(self).post(*self.path_args, **self.path_kwargs)
                if data:
                    if isinstance(data, tuple):
                        data = data[0]
                self.res = data and data or {}
            except NormalException as e:
                self.res = AutoError(e.code, e.message, e.ext).build_errors()
            except Exception:
                self.tracker.trace_error()
                self.status = 500
                self.error = True
        else:
            self.error = True

        if self.error:
            self.send_error(self.status)
        else:
            self._eval_custom_extension('res')
            if self.res is not None:
                self.res = self.build_res(self.res)
                self.write(self.res)
        if not self._finished:
            self.finish()

    @gen.coroutine
    def options(self, *args, **kwargs):
        if self.view:
            try:
                # ###----Node: params' handle----####
                # PrepareParams(self)()
                # self._eval_custom_extension('param')
                # ###----End Node: params' handle----####
                template = None
                kwargs = {}
                data = yield self.view(self).options(*self.path_args, **self.path_kwargs)
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
            self._eval_custom_extension('res')
            if self.res is not None:
                self.write(self.res)
        if not self._finished:
            self.finish()

    def build_res(self, res):
        if not isinstance(res, (str, bytes)):
            res = json.dumps(res, cls=JsonEncoder)
        return res
