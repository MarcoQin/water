#!/usr/bin/env python
# encoding: utf-8

import requests
import unittest
import time


import _env  # noqa
from water.utils.common_utils import pretty_print as pp
from water.constant.const_api_id import API_ID

url = "http://localhost:9000/"


class TestCalendar(unittest.TestCase):

    def test_update(self):
        headers = {"api_id": API_ID.CALENDAR.UPDATE}
        params = {
            "_id": "5721f39a421aa90726090971",
            'start': int(time.time())
        }
        res = requests.post(url, params, headers=headers)
        pp(res.text)

    def test_insert(self):
        headers = {"api_id": API_ID.CALENDAR.INSERT}
        params = {
            "user_id": 2,
            "start": int(time.time()) + 3600 * 24 * 9,
            "end": int(time.time()) + 3600 * 24 * 9 + 3600 * 1,
            "event": "测试数据",
            "description": "",
            "participant": "",
            "location": "Beijing China"
        }
        res = requests.post(url, params, headers=headers)
        pp(res.text)

    def test_list(self):
        headers = {"api_id": API_ID.CALENDAR.LIST}
        params = {'user_id': 1, 'participant': []}
        res = requests.post(url, params, headers=headers)
        #  pp(res.text)
        print res.text

    def test_new(self):
        headers = {"api_id": 10}
        params = {'user_id': 3, 'start': int(time.time()-3600*13*14)}
        res = requests.post(url, params, headers=headers)
        print res


if __name__ == "__main__":
    #  unittest.main()
    #  TestCalendar("test_insert").test_insert()
    TestCalendar("test_update").test_update()
    #  TestCalendar("test_list").test_list()
    #  TestCalendar("test_new").test_new()
