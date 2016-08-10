#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from water.utils.template_utils import AutoTemplate
from water.utils.web_utils import Redirect
from water.view.base_view import BaseView
from water.route.base_route import route, api_route
from water.utils.exception_utils import NormalException
from water.constant.const_api_id import API_ID
from water.constant.const_error import BaseError


@route('/hello(?:/)?(?P<name>.*)')
class HelloWorld(BaseView):

    @gen.coroutine
    def get(self, name='world'):
        if not name:
            return Redirect("/hello/world")
        return AutoTemplate(self), {'name': name}

    @gen.coroutine
    def post(self, name=""):
        rv = {'hello': name and name or 'world'}
        rv.update(self.arguments)
        return rv


@route("(?:/)?")
class Index(BaseView):

    @gen.coroutine
    def get(self):
        raise NormalException(BaseError.ERROR_PARAME_ERROR, 'Please visit <a href="/hello">here</a>')


@api_route(API_ID.HELLO_WORLD_API)
class HelloWorldAPI(BaseView):

    @gen.coroutine
    def post(self):
        raise NormalException(BaseError.ERROR_PARAME_ERROR, 'Please input name on url', this='api')
        return {'this': 'is', 'api': 'post'}
