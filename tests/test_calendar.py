#!/usr/bin/env python
# encoding: utf-8

import requests
import unittest
from datetime import datetime
import time


import _env  # noqa
from water.utils.common_utils import pretty_print as pp
from water.constant.const_api_id import API_ID


url = "http://localhost:9000/"
class TestCalendar(unittest.TestCase):

    def test_update(self):
        headers = {"api_id": API_ID.CALENDAR.UPDATE}
        params = {
            "_id": "5720c9ee5b8c372ecf8544ae",
            'start': int(time.time())
        }
        res = requests.post(url, params, headers=headers)
        pp(res.text)

    def test_insert(self):
        headers = {"api_id": API_ID.CALENDAR.INSERT}
        params = {
            "user_id": 1,
            "start": int(time.time()),
            "end": int(time.time()) + 3600,
            "event": "测试数据",
            "description": "",
            "participant": "",
            "location": "Beijing China"
        }
        res = requests.post(url, params, headers=headers)
        pp(res.text)

    def test_list(self):
        headers = {"api_id": API_ID.CALENDAR.LIST}
        params = {'user_id': 1}
        res = requests.post(url, params, headers=headers)
        pp(res.text)


if __name__ == "__main__":
    #  unittest.main()
    #  TestCalendar("test_insert").test_insert()
    #  TestCalendar("test_update").test_update()
    TestCalendar("test_list").test_list()
