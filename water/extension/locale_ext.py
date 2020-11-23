#!/usr/bin/env python
# encoding: utf-8

from water.extension.base_extension import ParamHandleExt


class GetLocale(ParamHandleExt):

    def __call__(self):
        this = self.handler
        headers = this.request.headers
        locale = 'en-us'
        if 'Accept-Language' in headers:
            locale = headers['Accept-Language'].lower()
        this.locale = locale
