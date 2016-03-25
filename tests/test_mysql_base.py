#!/usr/bin/env python
# encoding: utf-8

import unittest
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

import _env  # noqa
import water.model.mysql_base as base
from water.utils.common_utils import Dict


def setUpModule():
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


class TestCaseModel(base.Base):
    __tablename__ = 'mysql_base_testcase'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    create_time = Column(DateTime)


class TestMysqlBase(unittest.TestCase):
    def setUp(self):
        self.base = Dict({'create_time': datetime(2016, 1, 1, 0, 0),
                          'id': 1,
                          'name': 'test'})

    def test_Raw_query(self):
        Raw = base.Raw
        r = Raw.query_one('select * from mysql_base_testcase where id = 1;')
        self.assertDictEqual(r, self.base)

    def test_Model_query(self):

        self.assertDictEqual(TestCaseModel.query_one({'id': 1}).to_dict(), self.base)

    def test_Model_insert(self):
        now = datetime.now().strftime("%Y-%m-%d")
        data = {
            'id': 2,
            'name': 'test2',
            'create_time': now
        }
        TestCaseModel.delete({'id': 2})
        TestCaseModel.insert(data)
        self.assertDictEqual(TestCaseModel.query_one({'id': 2}).to_dict_str_mode('%Y-%m-%d'), data)

    def test_Model_update(self):
        now = datetime.now().strftime("%Y-%m-%d")
        data = {
            'id': 3,
            'name': 'test3',
            'create_time': now
        }
        TestCaseModel.delete({'id': 3})
        TestCaseModel.insert(data)
        self.assertDictEqual(TestCaseModel.query_one({'id': 3}).to_dict_str_mode('%Y-%m-%d'), data)
        TestCaseModel.update({'id': 3}, {'name': 'test3-mod'})
        self.assertEqual(TestCaseModel.query_one({'id': 3}).name, 'test3-mod')

    def test_Model_upsert(self):
        now = datetime.now().strftime("%Y-%m-%d")
        data = {
            'id': 4,
            'name': 'test4',
            'create_time': now
        }
        TestCaseModel.delete({'id': 4})
        TestCaseModel.upsert({'id': 4}, data)
        self.assertDictEqual(TestCaseModel.query_one({'id': 4}).to_dict_str_mode('%Y-%m-%d'), data)
        data['name'] = 'test4-upsert-mod'
        TestCaseModel.upsert({'id': 4}, data)
        self.assertEqual(TestCaseModel.query_one({'id': 4}).name, 'test4-upsert-mod')


if __name__ == "__main__":
    unittest.main()
