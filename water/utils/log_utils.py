#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import logging

from utils.common_utils import JsonEncoder


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
        self.logger.findCaller = self._findCaller

    def logging_request_header(self):
        pass

    def logging_request_body(self):
        pass

    def logging_response(self):
        pass

    def _pack_msg(self, msg_tag, msg_body):
        return "{0}: {1}".format(msg_tag, msg_body)

    def trace_error(self):
        etype, evalue, traceback = sys.exc_info()[:3]
        s = "ErrorStack:\n...Type: {0}\n...Value: {1}"
        self.logger.exception(s.format(etype, evalue))

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

    def _findCaller(self):
        '''
        Get caller info, to record (file, func, lineno)
        '''
        f = logging.currentframe()

        if f is not None:
            f = f.f_back.f_back
        rt = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rt = co.co_filename, f.f_lineno, co.co_name
            break
        return rt
