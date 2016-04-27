#!/usr/bin/env python
# encoding: utf-8

from tornado import gen

from constant.const_api_id import API_ID
from route.base_route import api_route
from view.base_view import BaseView

from model.calendar import Calendar


@api_route(API_ID.CALENDAR.LIST)
class List(BaseView):

    @gen.coroutine
    def post(self):
        user_id = int(self.arguments.user_id)
        participant = self.arguments.participant
        participant = [int(x) for x in participant] if participant else []
        u_ids = user_id
        if participant:
            u_ids = participant
            u_ids.append(user_id)
        return Calendar.get(u_ids)
        #  return list(col.find({'user_id': user_id}))
        #  return list(col.find({'user_id': user_id}, projection={'_id': 1}))


@api_route(API_ID.CALENDAR.INSERT)
class Insert(BaseView):

    @gen.coroutine
    def post(self):
        _id = Calendar.insert(self.arguments)
        return {'_id': _id}


@api_route(API_ID.CALENDAR.UPDATE)
class Update(BaseView):

    @gen.coroutine
    def post(self):
        _id = self.arguments.pop("_id", None)
        if not _id:
            return
        Calendar.update(_id, self.arguments)
