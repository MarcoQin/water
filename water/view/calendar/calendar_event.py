#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from constant.const_api_id import API_ID
from route.base_route import api_route
from view.base_view import BaseView

from model.mongo_base import get_db


@api_route(API_ID.CALENDAR)
class Calendar(BaseView):

    @gen.coroutine
    def post(self):
        col = get_db().calendar
        return {}
        return col.find_one({})
        return col.find_one(projection={'_id': 0})
