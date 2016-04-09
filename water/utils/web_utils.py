#!/usr/bin/env python
# encoding: utf-8


class Redirect(object):

    def __init__(self, url):
        self.url = url

    def do_redirect(self, handler):
        handler.redirect(self.url)
