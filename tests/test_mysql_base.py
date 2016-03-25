#!/usr/bin/env python
# encoding: utf-8

import json
import unittest
from datetime import datetime

import _env  # noqa
import water.model.mysql_base as base
from water.utils.common_utils import Dict


def setUpModule():
    print 'setUp'
    con, ctx = base.transaction_context()
    try:
        con.execute("DROP TABLE IF EXISTS mysql_base_testcase;")
        con.execute("create table mysql_base_testcase ( \
                    id int(11) primary key, name varchar(64), create_time datetime \
                    ) ENGINE=InnoDB CHARSET=utf8; ")
        con.execute("insert into mysql_base_testcase (id, name, create_time) \
                    values (1, 'test', '2016-01-01')")
        ctx.commit()
    except Exception:
        ctx.rollback()
    finally:
        if ctx:
            ctx.close()
        if con:
            con.close()


def tearDownModule():
    print "tearDown"
    con, ctx = base.transaction_context()
    try:
        con.execute("DROP TABLE IF EXISTS mysql_base_testcase;")
        ctx.commit()
    except Exception:
        ctx.rollback()
    finally:
        if ctx:
            ctx.close()
        if con:
            con.close()


class TestMysqlBase(unittest.TestCase):
    def setUp(self):
        self.base = Dict({'create_time': datetime(2016, 1, 1, 0, 0),
                          'id': 1,
                          'name': 'test'})

    def test_Raw_query(self):
        Raw = base.Raw
        r = Raw.query_one('select * from mysql_base_testcase where id = 1;')
        self.assertDictEqual(r, self.base)


if __name__ == "__main__":
    unittest.main()
