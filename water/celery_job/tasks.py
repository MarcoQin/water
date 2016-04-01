#!/usr/bin/env python
# encoding: utf-8

from celery_job.main import app


@app.task(name='celery_job.tasks.print_job')
def print_job(msg):
    print msg
