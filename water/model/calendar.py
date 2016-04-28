#!/usr/bin/env python
# encoding: utf-8

import time
from datetime import datetime

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
        @param kwargs
            start: int, timestamp
            end: int, timestamp
        """
        spec, start_t, end_t = cls.extract_spec(kwargs)
        fields = {}
        multiple = False
        if isinstance(user_ids, (int, basestring)):
            # single
            spec.update({"user_id": int(user_ids)})
        elif isinstance(user_ids, (list, tuple, set)):
            # multiple
            multiple = True
            spec.update({"user_id": {'$in': user_ids}})
            fields = {'_id': 1, 'start': 1, 'end': 1, 'user_id': 1, 'event': 1}
        res = {}
        if fields:
            rt = cls._db.calendar.find(spec, fields)
        else:
            rt = cls._db.calendar.find(spec)
        for ca in rt.sort('start'):
            print ca
            start = ca['start']
            end = ca['end']
            if start and end:
                t0 = datetime.fromtimestamp(start).strftime("%Y%m%dT%H")
                if t0 in res:
                    if not multiple:
                        res[t0].append(ca)
                else:
                    res[t0] = [ca]
                tr = (end - start) / 3600
                if tr > 1:
                    for i in range(tr):
                        tmp_t = start + (i + 1) * 3600
                        tmp_t = datetime.fromtimestamp(tmp_t).strftime("%Y%m%dT%H")
                        res[tmp_t] = [ca]
        res = cls.pack_res(res, start_t, end_t)
        return res

    @classmethod
    def pack_res(cls, res, start, end):
        rt = []
        fmt = "%Y%m%dT%H"
        f = lambda x: datetime.fromtimestamp(x).strftime(fmt)
        t = f(start)
        start_t = int(time.mktime(datetime.strptime(t, fmt).timetuple()))
        t = f(end)
        end_t = int(time.mktime(datetime.strptime(t, fmt).timetuple()))
        during = (end_t - start_t) / 3600
        for i in xrange(during):
            t_f = start_t + i * 3600
            t_f = f(t_f)
            rt.append(res.pop(t_f, []))
        print len(rt)
        return rt

    @classmethod
    def extract_spec(cls, data):
        n = datetime.now()
        n_str = n.strftime("%Y%m01")
        now = datetime.strptime(n_str, "%Y%m%d")
        e = "%.4d%.2d%.2d" % (n.year, n.month + 1, 1)
        e = datetime.strptime(e, "%Y%m%d")
        start = time.mktime(now.timetuple())
        end = time.mktime(e.timetuple())
        if 'start' in data and data['start']:
            start = int(data['start'])
        if 'end' in data and data['end']:
            end = int(data['end'])
        return {
            'start': {'$gte': start},
            'end': {'$lt': end},
        }, start, end

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
