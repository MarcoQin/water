#!/usr/bin/env python
# encoding: utf-8


class NormalException(Exception):
    """
    Pass formated errors from views by throw this exception
    """

    def __init__(self, code, message='Some thing happend!', **kwargs):
        self.code = code
        self.message = message
        self.ext = kwargs
