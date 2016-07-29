#!/usr/bin/env python
# encoding: utf-8

import weakref
import json

from weakref import WeakKeyDictionary
from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default  # replacement


class _Base(object):
    pass


class JsonFieldBase(object):
    pass


class JsonField(JsonFieldBase):

    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.type_is_Base = issubclass(field_type, _Base)
        self.default = default
        self.data = WeakKeyDictionary()

    def _set_value(self, instance, value):
        if self.type_is_Base:
            if instance in self.data:
                if isinstance(value, dict):
                    for k, v in value.iteritems():
                        self.data[instance].__setattr__(k, v)
                elif value is None:
                    self.data[instance] = self.field_type(None, outer=instance)
            else:
                self.data[instance] = self.field_type(value, outer=instance)
        else:
            if value is None:
                value = self._get_default()
            self.data[instance] = value

    def _get_value(self, instance):
        if instance in self.data:
            return self.data[instance]
        else:
            data = self._get_default()
            self._set_value(instance, data)
            return data

    def _get_default(self):
        data = self.default
        if callable(self.default):
            data = self.default()
            if not isinstance(data, self.field_type):
                if self.field_type == basestring:
                    data = str(data)
                else:
                    data = self.field_type(data)
        return data


class JsonMeta(type):
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        _obj = {}

        for k, v in attrs.iteritems():
            if isinstance(v, JsonFieldBase):
                _obj[k] = v
            else:
                newattrs[k] = v
        newattrs['_obj'] = _obj

        def __getattribute__(self, name):
            if name == '_obj':
                return _obj
            if name in _obj:
                tmp = _obj[name]
                if isinstance(tmp, _Base):
                    return tmp
                return tmp._get_value(self.outer())
            return object.__getattribute__(self, name)
        newattrs['__getattribute__'] = __getattribute__

        def __setattr__(self, name, value):
            if name in _obj:
                _obj[name]._set_value(self.outer(), value)
            else:
                object.__setattr__(self, name, value)
        newattrs['__setattr__'] = __setattr__

        def set_empty(self):
            for k, v in self._obj.iteritems():
                v._set_value(self.outer(), None)

        def _hook(self, **data):
            set_empty(self)
            for k, v in data.iteritems():
                self.__setattr__(k, v)
            return _obj

        def __init__(self, jsonstr, outer=None):
            if not outer:
                self.outer = weakref.ref(self)
            else:
                self.outer = weakref.ref(outer)

            if not jsonstr:
                data = {}
            else:
                data = json.loads(jsonstr)
            _hook(self, **data)
        newattrs['__init__'] = __init__

        def to_json(self):
            data = {}
            for k, v in _obj.iteritems():
                tmp = v._get_value(self.outer())
                if isinstance(tmp, _Base):
                    data[k] = tmp.to_json()
                else:
                    data[k] = tmp
            return data
        newattrs['to_json'] = to_json

        return super(JsonMeta, cls).__new__(cls, name, bases, newattrs)


class JsonBase(_Base):
    """
    Json Model的基类
    构建自己的json model类时继承此类，并创建class级的字段。如下:
    ```
        class CustomObject(JsonBase):
            b = JsonField(int)

        class NestObject(JsonBase):
            a = JsonField(CustomObject)

        class TestJsonObject(JsonBase):
            name = JsonField(basestring, default='')
            sample = JsonField(int, default=0)
            time = JsonField(int, default=time.time)
            data = JsonField(NestObject)
    ```
    上面的TestJsonObject即最终需要的类.
    实例化此类时，需要给init函数传入一个json string或者None
    ```
        result = TestJsonObject('{"name": "test", "sample": 2, "data": {"a": {"b": 1}}}')
    ```
    result 中的所有元素获取都被__getattribute__截获，可以以'.'符号获取
    result 有to_json方法, 返回为一个普通的dict（非json字符串)
    result 可以被json.dumps()正常序列化，推荐使用此方式
    """
    __metaclass__ = JsonMeta

    def __repr__(self):
        return str(self.to_json())
