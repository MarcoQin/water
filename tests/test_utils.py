#!/usr/bin/env python
# encoding: utf-8

import json
import unittest
from datetime import datetime

import _env  # noqa
import water.utils.common_utils as util


class TestUtilMethods(unittest.TestCase):

    def test_Dict(self):
        d = util.Dict()
        d.key = 'value'
        d['key1'] = 'value1'
        self.assertEqual(d['key'], d.key)
        self.assertEqual(d.key1, d['key1'])
        self.assertEqual(d.undifined, None)

    def test_classproperty(self):
        class A(object):
            @util.classproperty
            def name(cls):
                return 'classproperty'

        self.assertEqual(A.name, 'classproperty')

    def test_json_encoder(self):
        now = datetime.now()
        d = {
            'time': now
        }
        d1 = {
            'time': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.assertEqual(json.dumps(d, cls=util.JsonEncoder), json.dumps(d1))

if __name__ == "__main__":
    unittest.main()
