#!/usr/bin/env python
# encoding: utf-8

import _env  # noqa

import time
from water.celery_job.tasks import print_job

if __name__ == "__main__":
    print 'start', time.time()
    print_job.delay("hello world")
    print 'finish', time.time()
