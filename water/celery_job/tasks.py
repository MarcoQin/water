#!/usr/bin/env python
# encoding: utf-8

import time

from celery_job.main import app


@app.task(name='celery_job.tasks.print_job')
def print_job(msg):
    time.sleep(2)
    print "****From Celery****"
    print msg
    print "****From Celery****"
