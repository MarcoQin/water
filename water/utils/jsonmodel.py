#!/usr/bin/env python
# encoding: utf-8

import json

from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default  # replacement


class JsonFieldMeta(type):
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
                return _obj[name]._get_value()
            return object.__getattribute__(self, name)
        newattrs['__getattribute__'] = __getattribute__

        def __setattr__(self, name, value):
            if name in _obj:
                return _obj[name]._set_value(value)
        newattrs['__setattr__'] = __setattr__

        return super(JsonFieldMeta, cls).__new__(cls, name, bases, newattrs)


class JsonFieldBase(object):

    def _set_value(self, value):
        pass

    def _get_value(self):
        pass

    def to_json(self):
        pass


class JsonField(JsonFieldBase):

    def __init__(self, field_type, default=None):
        self.field_type = field_type
        self.default = default
        self.data = None

    def _set_value(self, value):
        if value is None or isinstance(value, self.field_type) or issubclass(value.__class__, self.field_type):
            self.data = value
        else:
            raise ValueError("filed_type not equal: %s" % value)

    def _get_value(self):
        if self.data is not None:
            return self.data
        else:
            if callable(self.default):
                data = self.default()
                if not isinstance(data, self.field_type):
                    if self.field_type == basestring:
                        data = str(data)
                    else:
                        data = self.field_type(data)
                return data
            return self.default

    def to_json(self):
        return self._get_value()


class JsonObjectField(JsonFieldBase):
    __metaclass__ = JsonFieldMeta

    def _set_value(self, value):
        if isinstance(value, dict):
            for k, v in value.iteritems():
                if k in self._obj:
                    field = self._obj[k]
                    if isinstance(field, JsonFieldBase):
                        field._set_value(v)
        if value is None:
            for k in self._obj.iterkeys():
                self._obj[k]._set_value(None)

    def _get_value(self):
        return self
        data = {}
        for k, v in self._obj.iteritems():
            if isinstance(v, JsonField):
                data[k] = v._get_value()
        return data

    def to_json(self):
        data = {}
        for k, v in self._obj.iteritems():
            if isinstance(v, JsonFieldBase):
                data[k] = v._get_value()
        return data

    def __repr__(self):
        return str(self.to_json())


class JsonMeta(type):
    def __new__(cls, name, bases, attrs):
        newattrs = {}
        __obj = {}

        for k, v in attrs.iteritems():
            if isinstance(v, JsonFieldBase):
                __obj[k] = v
            else:
                newattrs[k] = v
        newattrs['__obj'] = __obj

        def __getattribute__(self, name):
            if name == '__obj':
                return __obj
            if name in __obj:
                return __obj[name]._get_value()
            return object.__getattribute__(self, name)
        newattrs['__getattribute__'] = __getattribute__

        def __setattr__(self, name, value):
            if name in __obj:
                return __obj[name]._set_value(value)
        newattrs['__setattr__'] = __setattr__

        def _hook(**data):
            for k, v in data.iteritems():
                if k in __obj:
                    __obj[k]._set_value(v)
            if not data:
                # init
                for k, v in __obj.iteritems():
                    __obj[k]._set_value(None)
            return __obj

        def __init__(self, jsonstr):
            if not jsonstr:
                data = {}
            else:
                data = json.loads(jsonstr)
            _hook(**data)
        newattrs['__init__'] = __init__

        def to_json(self):
            data = {}
            for k, v in __obj.iteritems():
                data[k] = v._get_value()
            return data
        newattrs['to_json'] = to_json

        return super(JsonMeta, cls).__new__(cls, name, bases, newattrs)


class JsonBase(object):
    """
    Json Model的基类
    构建自己的json model类时继承此类，并创建class级的字段。如下:
    ```
        class CustomObject(JsonObjectField):
            b = JsonField(int)

        class NestObject(JsonObjectField):
            a = CustomObject()

        class TestJsonObject(JsonBase):
            name = JsonField(basestring, default='')
            sample = JsonField(int, default=0)
            time = JsonField(int, default=time.time)
            data = NestObject()
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
