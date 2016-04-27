#!/usr/bin/env python
# encoding: utf-8

import time

from bson import ObjectId
from mongo_base import get_db
from utils.common_utils import classproperty


class Calendar(object):
    """
    {
        "_id": ObjectId,  # unique, primary_key
        "user_id": int,  # user_id
        "create_time": int,  # timestamp
        "modify_time": int,  # timestamp
        "start": int,  # timestamp
        "end": int,  # timestamp
        "event": string,  # event title
        "description": string,  # description
        "participant": [],  # list of user_ids
        "location": string,  # location
        "alert_time": int,  # timestamp
    }
    """

    @classproperty
    def default(cls):
        return {
            "create_time": int(time.time()),
            "modify_time": 0,
            "start": 0,
            "end": 0,
            "event": "",
            "description": "",
            "participant": [],  # list of user_ids
            "location": "",
            "alert_time": 0,
        }

    _db = get_db()

    @classmethod
    def insert(cls, data):
        res = cls.default
        res.update(cls.verify_data(data))
        _id = cls._db.calendar.insert_one(res).inserted_id
        return _id

    @classmethod
    def update(cls, _id, data):
        if not _id:
            return
        if isinstance(_id, basestring):
            _id = ObjectId(_id)
        res = {}
        op_mapping = cls.op_mapping
        for k, v in data.iteritems():
            if k in op_mapping:
                res[k] = op_mapping[k](v)
        res["modify_time"] = time.time()
        cls._db.calendar.update_one({'_id': _id}, res)

    @classmethod
    def get(cls, user_ids, **kwargs):
        """
        start: int, timestamp
        end: int, timestamp
        """
        if isinstance(user_ids, int):
            # single
            pass
        elif isinstance(user_ids, (list, tuple, set)):
            # multiple
            pass

    @classproperty
    def op_mapping(cls):
        f = lambda x: int(float(x)) if x else 0
        f1 = lambda x: x if x else ""
        op_mapping = {
            "user_id": f,
            "start": f,
            "end": f,
            "alert_time": f,
            "event": f1,
            "description": f1,
            "participant": lambda x: [int(y) for y in x] if x else [],
            "location": lambda x: x if x else "",
        }
        return op_mapping

    @classmethod
    def verify_data(cls, data):
        new = {}
        for k, v in cls.op_mapping.iteritems():
            if k in data:
                new[k] = v(data[k])
        return new
