#!/usr/bin/env python
# encoding: utf-8

import unittest

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

if __name__ == "__main__":
    unittest.main()
