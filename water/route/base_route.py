#!/usr/bin/env python
# encoding: utf-8

import re

ALL_ROUTES = []


def route(url):
    def _view(cls):
        ALL_ROUTES.append((re.compile(url), cls))
        return cls
    return _view
