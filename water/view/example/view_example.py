#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from utils.common_utils import classproperty
from utils.template_utils import AutoTemplate
from view.base_view import BaseView
from route.base_route import route
from extension.base_extension import PrepareExt
from utils.exception_utils import NormalException


class PrepareParams(PrepareExt):

    def __call__(self):
        print "custom Extension"
        print self.handler.request.path


@route('/hello(?:/)?(?P<name>.*)')
class HelloWorld(BaseView):

    @gen.coroutine
    def get(self, name='world'):
        if not name:
            raise NormalException('Please input name on url')
            self.handler.redirect("/hello/world")
            return None
        return AutoTemplate(self), {'name': name}

    @gen.coroutine
    def post(self, name=""):
        return {'hello': name and name or 'world'}

    @classproperty
    def extensions(cls):
        return PrepareParams
