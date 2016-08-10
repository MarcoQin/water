#!/usr/bin/env python
# encoding: utf-8

import time

from water.celery_job.main import app
from water.utils.common_utils import Dictlise


@app.task()
def print_job(msg):
    time.sleep(2)
    print "****From Celery****"
    print msg
    print "****From Celery****"
    a = {'a': 'b'}
    a = Dictlise(a)
    print a
