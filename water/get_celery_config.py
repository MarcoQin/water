#!/usr/bin/env python
# encoding: utf-8

import sys


Default = dict(
    pidfile='~/data/celery/%n.pid',
    logfile='~/data/celery/%n%I.log'
)

USE_DEFAULT = False

try:
    from config.config import Celery
except ImportError:
    USE_DEFAULT = True
    Celery = Default
else:
    if not Celery:
        USE_DEFAULT = True
        Celery = Default

if __name__ == "__main__":
    arg = sys.argv[1]
    if not USE_DEFAULT:
        print >> sys.stderr, "\033[32mGet Config {} from config.config\033[0m".format(arg)
    else:
        print >> sys.stderr, "\033[31mWARNING: Can't find {} from config, Use default config\033[0m".format(arg)
    print Celery[arg]
