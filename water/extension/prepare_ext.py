#!/usr/bin/env python
# encoding: utf-8

from base_extension import PrepareExt
from route.base_route import ALL_ROUTES


class FindView(PrepareExt):

    def __call__(self):
        path = self.handler.request.path
        for _regex, _view in ALL_ROUTES:
            if _regex.match(path):
                self.handler.view = _view
                break
