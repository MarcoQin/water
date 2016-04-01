#!/usr/bin/env python
# encoding: utf-8

import json

from extension.base_extension import ParamHandleExt, PrepareExt, FinishExt


class PrepareParams(ParamHandleExt):

    def _extract_first_arg(self, args):
        rv = {}
        for k, v in args.items():
            rv[k] = v[0]
        return rv

    def __call__(self):
        this = self.handler
        if this.request.method == 'POST':
            if this.request.body:
                try:
                    this.arguments = json.loads(this.request.body)
                except ValueError:
                    this.arguments = self._extract_first_arg(this.request.body_arguments)
        elif this.request.method == 'GET':
            this.arguments = self._extract_first_arg(this.request.query_arguments)


class RequestLog(PrepareExt):

    def __call__(self):
        this = self.handler
        this.tracker.logging_request_header(this)
        this.tracker.logging_request_body(this)


class ResponseLog(FinishExt):

    def __call__(self):
        this = self.handler
        if this.request.method == "POST":
            this.tracker.logging_response(this)
