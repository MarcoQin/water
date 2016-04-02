#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from utils.common_utils import classproperty
from utils.template_utils import AutoTemplate
from view.base_view import BaseView
from route.base_route import route, api_route
from utils.exception_utils import NormalException
from extension.common_ext import PrepareParams, RequestLog, ResponseLog
from constant.const_api_id import API_ID


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
        rv = {'hello': name and name or 'world'}
        rv.update(self.arguments)
        return rv

    @classproperty
    def extensions(cls):
        return PrepareParams, RequestLog, ResponseLog


@api_route(API_ID.HELLO_WORLD_API)
class HelloWorldAPI(BaseView):

    @gen.coroutine
    def post(self):
        return {'this': 'is', 'api': 'post'}

    @classproperty
    def extensions(cls):
        return PrepareParams, RequestLog, ResponseLog
