#!/usr/bin/env python
# encoding: utf-8

import json
from datetime import datetime, date


class Dict(dict):
    """
    Object-like dict
    """
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


def to_dict_str_mode(self, time_format=None, keys=None):
    info = self.to_dict(keys=keys)
    for k, v in info.iteritems():
        if k in ('to_dict', 'to_dict_str_mode'):
            continue
        if v is None:
            info[k] = ''
        elif isinstance(v, datetime):
            if time_format:
                info[k] = v.strftime(time_format)
            else:
                info[k] = str(v)
    return info


def to_dict(self, keys=None):
    """
    :type keys: list, tuple, set, iterable objects
    """
    if keys:
        return Dict({name: getattr(self, name)
                    for name in keys})
    return self


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
