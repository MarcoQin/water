#!/usr/bin/env python
# encoding: utf-8

from utils.common_utils import classproperty
from view.base_view import BaseView
from route.base_route import route
from extension.base_extension import PrepareExt


class PrepareParams(PrepareExt):

    def __call__(self):
        print "custom Extension"
        print self.handler.request.path


@route('/hello')
class Hello(BaseView):

    def get(self):
        return "hello world"

    @classproperty
    def extensions(cls):
        return PrepareParams
