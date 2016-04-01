#!/usr/bin/env python
# encoding: utf-8


from celery import Celery

from config.config import REDIS_CONFIG

redis_url = 'redis://:{password}@{host}:{port}/{db}'.format(**REDIS_CONFIG)

app = Celery(
    'celery_job',
    broker=redis_url,
    include=['celery_job.tasks']
)


if __name__ == "__main__":
    app.start()
