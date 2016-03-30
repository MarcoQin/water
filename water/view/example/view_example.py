#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from utils.common_utils import classproperty
from view.base_view import BaseView
from route.base_route import route
from extension.base_extension import PrepareExt


class PrepareParams(PrepareExt):

    def __call__(self):
        print "custom Extension"
        print self.handler.request.path


@route('/hello(?:/)?(?P<name>.*)')
class Hello(BaseView):

    @gen.coroutine
    def get(self, name='world'):
        if not name:
            name = 'world'
            return "hello " + name
        return self.handler.redirect("/hello")

    @classproperty
    def extensions(cls):
        return PrepareParams
