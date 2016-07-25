#!/usr/bin/env python
# encoding: utf-8

import json
import unittest
from datetime import datetime

import _env  # noqa
import water.utils.common_utils as util
import water.utils.web_utils as web_util


class TestUtilMethods(unittest.TestCase):

    def test_Dict(self):
        d = util.Dict()
        d.key = 'value'
        d['key1'] = 'value1'
        self.assertEqual(d['key'], d.key)
        self.assertEqual(d.key1, d['key1'])
        self.assertEqual(d.undifined, None)

    def test_Dictlise(self):
        f = util.Dictlise
        l = [{'a': 1, 'b': 2}]
        d = {"l": [{'a': 1, 'b': 2}]}
        d1 = {"l": [{'a': 1, 'b': 2, 'c': [{'a': 1}]}]}
        l = f(l)
        self.assertEqual(l[0].a, 1)
        self.assertEqual(l[0].b, 2)
        d = f(d)
        self.assertEqual(d.l[0].a, 1)
        self.assertEqual(d.l[0].b, 2)
        d1 = f(d1)
        self.assertEqual(d1.l[0].a, 1)
        self.assertEqual(d1.l[0].b, 2)
        self.assertEqual(d1.l[0].c[0].a, 1)

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

    def test_camel_convert(self):
        a = "ThisIsCamelCase"
        b = "this_is_camel_case"
        self.assertEqual(util.camel_convert(a), b)

    def test_get_redirect_location(self):
        url = "https://www.baidu.com/link?url=pAitIllTlAEgTICGhIO-yFK90W7_7ZRmesMGumGYSHLY7dWy3uHIlLrvHvxb5wJ12eluBi40k95zILWa2K_xsa"
        target = "http://tech.qq.com/a/20160718/027826.htm"
        r = web_util.WebUtils.get_redirect_location(url)
        self.assertEqual(r, target)

if __name__ == "__main__":
    unittest.main()
