#!/usr/bin/env python
# encoding: utf-8

from gevent import monkey
monkey.patch_all()

from celery import Celery
from celery import current_app
from celery.signals import after_task_publish

from config.config import REDIS_CONFIG

redis_url = 'redis://{host}:{port}/{db}'.format(**REDIS_CONFIG)


app = Celery(
    'celery_job',
    broker=redis_url,
    backend=redis_url,
    include=['celery_job.tasks']
)

app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    BROKER_TRANSPORT_OPTIONS={'fanout_prefix': True, 'fanout_patterns': True},
)


@after_task_publish.connect
def update_sent_state(sender=None, body=None, **kwargs):
    # the task may not exist if sent using `send_task` which
    # sends tasks by name, so fall back to the default result backend
    # if that is the case.
    task = current_app.tasks.get(sender)
    backend = task.backend if task else current_app.backend
    backend.store_result(body['id'], None, "SENT")


if __name__ == "__main__":
    app.start()
