#!/usr/bin/env python
# encoding: utf-8

from mongo_base import get_db


class User(object):
    """
    {
        "_id": int, # user_id
        "name": string,
        "email": string,
        "friends": [],
    }
    """

    _db = get_db()

    @classmethod
    def get_friends_id(cls, user_id):
        u_info = cls._db.user.find_one({'_id': user_id})
        friends = u_info['friends']
        return friends
