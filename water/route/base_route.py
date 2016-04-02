#!/usr/bin/env python
# encoding: utf-8

import re

ALL_ROUTES = []
API_HANDLER_MAP = {}


def route(url):
    if not url.endswith('$'):
        url += '$'

    def _view(cls):
        ALL_ROUTES.append((re.compile(url), cls))
        return cls
    return _view


def api_route(api_id):

    def _view(cls):
        API_HANDLER_MAP[int(api_id)] = cls
        return cls
    return _view
