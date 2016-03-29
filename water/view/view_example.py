#!/usr/bin/env python
# encoding: utf-8

from base_view import BaseView
from route.base_route import route


@route('/hello')
class Hello(BaseView):

    def get(self):
        return "hello world"
