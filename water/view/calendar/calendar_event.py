#!/usr/bin/env python
# encoding: utf-8

import time
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
        return Calendar.get(u_ids, **self.arguments)
        #  return list(col.find({'user_id': user_id}))
        #  return list(col.find({'user_id': user_id}, projection={'_id': 1}))


@api_route(API_ID.CALENDAR.INSERT)
class Insert(BaseView):

    @gen.coroutine
    def post(self):
        _id = Calendar.insert(self.arguments)
        return {'_id': _id}


@api_route(10)
class New(BaseView):

    @gen.coroutine
    def post(self):
        user_id = int(self.arguments.user_id)
        start = int(float(self.arguments.start))
        data = {
            "user_id": user_id,
            "create_time": int(time.time()),
            "modify_time": 0,
            "start": 0,
            "end": 0,
            "event": "User: {} Text".format(user_id),
            "description": "no description",
            "participant": [],  # list of user_ids
            "location": "北京",
            "alert_time": 0,
        }
        for i in xrange(50):
            data['start'] = start
            data['end'] = start + 3600
            Calendar.insert(data)
            start += 3600 * 6
        return {}


@api_route(11)
class Clear(BaseView):

    @gen.coroutine
    def post(self):
        user_id = int(self.arguments.user_id)
        Calendar._db.calendar.remove({'user_id': user_id})
        return {}


@api_route(API_ID.CALENDAR.UPDATE)
class Update(BaseView):

    @gen.coroutine
    def post(self):
        _id = self.arguments.pop("_id", None)
        if not _id:
            return
        Calendar.update(_id, self.arguments)
