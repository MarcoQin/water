#!/usr/bin/env python
# encoding: utf-8


class BaseExtension(object):

    def __init__(self, handler, *args, **kwargs):
        self.handler = handler

    def __call__(self):
        return None


class PrepareExt(BaseExtension):

    def __init__(self, handler, *args, **kwargs):
        super(PrepareExt, self).__init__(handler, *args, **kwargs)

    def __call__(self):
        return None


class FinishExt(BaseExtension):

    def __init__(self, handler, *args, **kwargs):
        super(FinishExt, self).__init__(handler, *args, **kwargs)

    def __call__(self):
        return None


class ParamHandleExt(BaseExtension):

    def __init__(self, handler, *args, **kwargs):
        super(ParamHandleExt, self).__init__(handler, *args, **kwargs)

    def __call__(self):
        return None
