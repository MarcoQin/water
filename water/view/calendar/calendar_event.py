#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from constant.const_api_id import API_ID
from route.base_route import api_route
from view.base_view import BaseView


@api_route(API_ID.CALENDAR)
class Calendar(BaseView):

    @gen.coroutine
    def post(self):
        return {'code': 200}
