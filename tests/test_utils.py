#!/usr/bin/env python
# encoding: utf-8

import water.utils.common_utils as util


def test_Dict():
    d = util.Dict()
    d.key = 'value'
    print d
    assert d['key'] == d.key

if __name__ == "__main__":
    test_Dict()
