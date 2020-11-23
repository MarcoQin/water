#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import logging
import json

from water.utils.common_utils import JsonEncoder


if hasattr(sys, 'frozen'):
    _srcfile = "utils%slog_utils%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)


class LogTracker(object):

    def __init__(self, logger='track'):

        self.logger = logging.getLogger(logger)
        # because of this wrapper of logger, logging info will not find the right
        # info of the caller. solve this by rewrite the findCaller function
        # self.logger.findCaller = self._findCaller

    def logging_request_header(self, handler):
        '''
        append record request header in log file
        '''

        try:
            method = handler.request.method
            #  header_msg = json.dumps(dict(handler.request.headers)).decode('unicode_escape')
            header_msg = json.dumps(dict(handler.request.headers))
            self.logger.debug(self._pack_msg('%s::RequestHeader' % method, header_msg))
        except:
            self.trace_error()

    def logging_request_body(self, handler):
        '''
        record request header in log file
        '''

        try:
            method = handler.request.method
            header_msg = json.dumps(dict(handler.request.headers))
            if method == "GET":
                body_msg = ';'.join("%s: %s" % (k, v) for k, v in handler.request.query_arguments.items())
            else:
                body = handler.request.body
                if isinstance(body, bytes):
                    try:
                        body = body.decode()
                    except Exception:
                        body = 'cannot decode body'
                body_msg = body.replace('\n', '').replace('\r', '')
            #  body_msg = handler.request.body.decode('unicode_escape').replace('\n', '')
            self.logger.debug(self._pack_msg('%s::RequestHeader:%s \nRequestBody' % (method, header_msg), body_msg))
        except:
            self.trace_error()

    def logging_response(self, handler):
        '''
        record response in log file
        '''

        try:
            method = handler.request.method
            if not isinstance(handler.res, (str, bytes)):
                #  response_msg = json.dumps(handler.res, cls=JsonEncoder).decode('unicode_escape')
                response_msg = json.dumps(handler.res, cls=JsonEncoder, ensure_ascii=False)
            else:
                response_msg = handler.res
            self.logger.debug(self._pack_msg('%s::ResponseMsg' % method, response_msg))
        except:
            self.trace_error()

    def _pack_msg(self, msg_tag, msg_body):
        return "%s: %s" % (msg_tag, msg_body)

    def trace_error(self):
        etype, evalue, traceback = sys.exc_info()[:3]
        s = "ErrorStack:\n...Type: %s\n...Value: %s"
        self.logger.exception(s % (etype, evalue))

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def exception(self, e):
        self.logger.exception(e)

    def _findCaller(self, stack_info=False):
        '''
        Get caller info, to record (file, func, lineno)
        '''
        f = logging.currentframe()

        if f is not None:
            f = f.f_back.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = co.co_filename, f.f_lineno, co.co_name
            break
        return rv
