#!/usr/bin/env python
# encoding: utf-8

from handler.base_handler import MainHandler

handlers = [
    (r'.*', MainHandler),
]
