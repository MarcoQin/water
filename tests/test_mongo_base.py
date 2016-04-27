#!/usr/bin/env python
# encoding: utf-8

import unittest
from datetime import datetime

import _env  # noqa
import water.model.mongo_base as base
from water.utils.common_utils import Dict


class TestMongoBase(unittest.TestCase):

    def test_get_collection(self):
        db = base.get_db()
        col = db.calendar
        print col.find_one({})
        print col.find({})


if __name__ == "__main__":
    unittest.main()
