#!/usr/bin/env python
# encoding: utf-8

import json
import time
import datetime
import itertools

from sqlalchemy import create_engine, or_, desc
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import types

from config import config
from utils.common_utils import Dict


_connection_uri = "mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8".format(
    **config.MYSQL_CONFIG)

_engine = create_engine(_connection_uri, encoding='utf-8', pool_recycle=300,  # this value should little than mysql's connect_timeout
                        isolation_level="READ UNCOMMITTED")  # When the SQLAlchemy engine is started with the "READ UNCOMMITED" isolation_level it will perform "dirty reads" which means it will read uncommited changes directly from the database.

_session_factory = sessionmaker(bind=_engine)

_Session = scoped_session(_session_factory)


def get_session():
    """
    If you need more complex query like join or select,
    just use this function and through session to get them.  """
    _Session.rollback()
    return _Session


def transaction_context():
    """
    mysql transaction context

    Usage:
        >>> connection, ctx = transaction_context()
        >>> try:
        ...     # do some insertion or update here
        ...     connection.execute("insert into x (a, b) values (1, 2)")
        ...     ctx.commit()
        ... except Exception:
        ...     ctx.rollback()
        ... finally:
        ...     if ctx:
        ...         ctx.close()
        ...     if connection:
        ...         connection.close()
        ...
    """
    con = _engine.connect()
    return con, con.begin()


op_mapping = {
    '=': (lambda cls, k, v: getattr(cls, k) == v),
    '$eq': (lambda cls, k, v: getattr(cls, k) == v),
    '!=': (lambda cls, k, v: getattr(cls, k) != v),
    '$ne': (lambda cls, k, v: getattr(cls, k) != v),
    '>': (lambda cls, k, v: getattr(cls, k) > v),
    '$gt': (lambda cls, k, v: getattr(cls, k) > v),
    '>=': (lambda cls, k, v: getattr(cls, k) >= v),
    '$gte': (lambda cls, k, v: getattr(cls, k) >= v),
    '<': (lambda cls, k, v: getattr(cls, k) < v),
    '$lt': (lambda cls, k, v: getattr(cls, k) < v),
    '<=': (lambda cls, k, v: getattr(cls, k) <= v),
    '$lte': (lambda cls, k, v: getattr(cls, k) <= v),
    '$or': (lambda cls, k, v: or_(getattr(cls, k) == value for value in v)),
    '$in': (lambda cls, k, v: getattr(cls, k).in_(v)),
    '$nin': (lambda cls, k, v: ~getattr(cls, k).in_(v)),
    '$like': (lambda cls, k, v: getattr(cls, k).like('%{}%'.format(v))),
    '$nlike': (lambda cls, k, v: ~getattr(cls, k).like(v)),
    '+': (lambda cls, k, v: getattr(cls, k) + v),
    '$incr': (lambda cls, k, v: getattr(cls, k) + v),
    '-': (lambda cls, k, v: getattr(cls, k) - v),
    '$decr': (lambda cls, k, v: getattr(cls, k) - v),
}


def parse_operator(cls, op_dict):
    binary_expressions = []
    for k, v in op_dict.iteritems():
        if not isinstance(v, dict):
            binary_expressions.append(getattr(cls, k) == v)
        else:
            for k1, v1 in v.iteritems():
                if k1 in op_mapping:
                    binary_expressions.append(op_mapping[k1](cls, k, v1))
    return binary_expressions


def map_operator(key, value_dict):
    if '$incr' in value_dict:
        return key + value_dict['$incr']
    elif '$decr' in value_dict:
        return key - value_dict['$decr']


row2dict = lambda r: Dict({c.name: getattr(r, c.name)
                           for c in r.__table__.columns})


def row2dict_parse(info):
    info = row2dict(info)
    for k, v in info.iteritems():
        if v is None:
            info[k] = ''
        elif isinstance(v, datetime.datetime):
            info[k] = str(v)
    return info


def row2dict_timestamp_mode(info):
    info = row2dict(info)
    for k, v in info.iteritems():
        if v is None:
            info[k] = ''
        elif isinstance(v, datetime.datetime):
            info[k] = time.mktime(v.timetuple())
    return info


@as_declarative()
class Base(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    _session = get_session()
    _session()

    @classmethod
    def get(cls, pk):
        """
        query by primary_key
        """
        return cls._session.query(cls).get(pk)

    @classmethod
    def query(
            cls,
            condition=None,
            order_by=None,
            distinct=None,
            offset=None,
            limit=None,
            skip_slice=False):
        """
        Params:
            condition: dict
                Usage:
                    >>> condition = {
                    ...     'name': 'test',
                    ...     'avatar_id': {'$gt':1000, '$lt':5000},
                    ...     'id': {'$in':[123,1234,12345]}
                    ...     }
                    ...
                    >>> result = TestModel.query(condition, limit=1)

            order_by:
                    ASC:
                        type(str) : 'name'
                        type(list, tuple): ('name', 1) or ('name', 1, 'create_time', 1)
                    DESC:
                        type(list, tuple): ('name', -1)
                        type(list, tuple): ('name', -1) or ('name', -1, 'create_time', -1)

            distinct:
                param:
                    type(str): 'name'
                return:
                    list of tuples:
                        >>> r = TestModel.query({'name':'test'},distinct='name')
                        >>> r
                        >>> [('test', )]

            skip_slice: type(bool):
                if this value is True, r will been returned else return r[offset:offset+limit]
                type(r) is <class 'sqlalchemy.orm.query.Query'>, not the query results.

        Return:
            list of query results
        """
        if condition is None:
            condition = {}
        p = parse_operator(cls, condition)
        if distinct:
            r = cls._session.query(
                getattr(
                    cls, distinct)).filter(
                *p).distinct()
        else:
            r = cls._session.query(cls).filter(*p)
        if order_by:
            if isinstance(order_by, (list, tuple)):
                i = 1
                tmp = order_by[:2]
                while(tmp):
                    if tmp[-1] > 0:
                        r = r.order_by(tmp[0])
                    else:
                        r = r.order_by(desc(tmp[0]))
                    tmp = order_by[2 * i: (i + 1) * 2]
                    i += 1
            else:
                r = r.order_by(order_by)
        if skip_slice:
            return r
        if offset and limit:
            limit = offset + limit
        try:
            ret = r[offset:limit]
        except:
            cls._session.close()
            ret = r[offset:limit]

        return ret

    @classmethod
    def query_one(cls, condition=None, order_by=None):
        """
        Params:
            just see _query

        Return:
            query result
        """
        r = cls.query(condition, order_by=order_by, limit=1)

        return r[0] if r else Dict()

    @classmethod
    def insert(cls, data, is_transaction=False):
        """
        data:
            dict: {'name':'test_name', 'avatar_id':123123}

            or:

            list: [{'name':'test1', 'avatar_id':123123}, {'name':'test', 'avatar_id':123123}]
        """
        if isinstance(data, list):
            r = [cls(**meta) for meta in data]
            cls._session.add_all(r)
        else:
            r = cls(**data)
            cls._session.add(r)

        if not is_transaction:
            cls._session.commit()

        return r

    @classmethod
    def count(cls, condition=None, distinct=None):
        r = cls.query(condition, distinct=distinct, skip_slice=True)
        return r.count()

    @classmethod
    def update(cls, condition=None, update_data=None, is_transaction=False, extra_update_options=None):
        """
        update_data:
            type(dict)
            {
                'name':'test',  # normal change should use dot operator
                'age': {'$incr': 10},  # for increment: age = age + 10
                'money': {'$decr': 20}  # for decrement: age = age - 10
            }
        """
        r = cls.query(condition, skip_slice=True)
        for k, v in update_data.items():
            if isinstance(v, dict):
                for k1, v1 in v.iteritems():
                    if k1 in op_mapping:
                        update_data[k] = op_mapping[k1](cls, k, v1)
        if not extra_update_options:
            extra_update_options = {}
        r = r.update(update_data, **extra_update_options)

        if not is_transaction:
            cls._session.commit()
        return r

    @classmethod
    def _merge(cls, old, new, is_transaction=False):
        for k, v in new.iteritems():
            setattr(old, k, v)

        if not is_transaction:
            old.save()

    @classmethod
    def upsert(cls, condition=None, update_data=None, multi=False, is_transaction=False):
        """
        upsert method
        Advance updating is not supported.

        :param condition: dict, like query's condition
        :param update_data: dict, only support simple dict{'user_id': '123123'}
        :param multi: bool, multiple upsert is supported.
        """
        r = cls.query(condition, skip_slice=True)
        if multi:
            r = r[:]
        else:
            r = r[:1]
        if not r:
            if condition:
                update_data.update(condition)
            r = cls.insert(update_data, is_transaction)
        else:
            if multi:
                for item in r:
                    cls._merge(item, update_data, is_transaction)
            else:
                r = r[0]
                cls._merge(r, update_data, is_transaction)
        return r

    @classmethod
    def delete(cls, condition=None, is_transaction=False, synchronize_session='evaluate'):
        r = cls.query(condition, skip_slice=True)
        r = r.delete(synchronize_session=synchronize_session)

        if not is_transaction:
            cls._session.commit()
        return r

    def save(self):
        """
        Use this method after you've modified data to ensure new data will been commited
        """
        if self._session.dirty:
            self._session.commit()

    def __repr__(self):
        s = "<%s(" % self.__tablename__
        for k, v in self.__dict__.iteritems():
            if not k.startswith('_'):
                s += "%s=%s, " % (k, v)
        s = s[:-2]
        s += ")>"
        return s

    def to_dict(self, keys=None):
        """
        :type keys: list, tuple, set, iterable objects
        """
        if keys:
            return Dict({name: getattr(self, name)
                         for name in keys})
        return Dict({c.name: getattr(self, c.name)
                    for c in self.__table__.columns})

    def to_json(self):
        return json.dumps(row2dict_parse(self))

    def to_dict_str_mode(self, time_format=None, keys=None):
        info = self.to_dict(keys=keys)
        for k, v in info.iteritems():
            if v is None:
                info[k] = ''
            elif isinstance(v, datetime.datetime):
                if time_format:
                    info[k] = v.strftime(time_format)
                else:
                    info[k] = str(v)
        return info

    def to_dict_timestamp_mode(self):
        return row2dict_timestamp_mode(self)


class Raw(object):
    """
    Provide Raw SQL query execute
    Return Dict instance
    """
    _session = get_session()

    @classmethod
    def _execute(cls, sql, params=None):
        try:
            return cls._session.execute(sql, params)
        finally:
            cls._session.remove()

    @classmethod
    def query_one(cls, sql, params=None):
        r = cls.query(sql, params)
        if r:
            return r[0]
        return Dict()

    @classmethod
    def query(cls, sql, params=None):
        """
        :param sql: raw SQL
        :param params: dict

        >>> Raw.query_one('select * from test where user_id = :user_id', {'user_id': 123123})
        >>> Raw.query('select user_id, avatar_id from test_table')
        """
        result = cls._execute(sql, params)
        column_names = result.keys()
        return [Dict(itertools.izip(column_names, row))
                for row in result.fetchall()]


class JsonType(types.TypeDecorator):
    """
    自定义的Json数据类型,对应mysql中存储的text字段.
    使用方式如下：
        class TestModel(Base):
            extra = Column(JsonType(TestJsonObject))
    实例化需要传入一个继承util.jsonmodel.JsonBase的自定义json类, 如上述的TestJsonObject
    使用query_one 或 query拿到的结果, 如result，将包含一个叫extra的字段。
    更新result的extra时, 可以将extra中需要更新的东西更改之后，再result.extra = result.extra.to_json() & result.save()
    不过还是推荐使用TestModel.update()的方式。update extra时可以传入TestJsonObject实例、string、dict等。
    如： TestModel.update({'id': 1}, {'extra': TestJsonObject(None)})
    """

    impl = types.Text

    def __init__(self, json_model=None):
        self.json_model = json_model
        super(JsonType, self).__init__()

    def process_bind_param(self, value, dialect):
        if value is None:
            data = json.dumps(self.json_model(None))
        elif isinstance(value, basestring):
            data = value
        else:
            data = json.dumps(value)
        return data

    def process_result_value(self, value, dialect):
        return self.json_model(value)
