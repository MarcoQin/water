#!/usr/bin/env python
# encoding: utf-8

import json

from water.extension.base_extension import ParamHandleExt, PrepareExt, FinishExt, ResHandleExt
from water.utils.common_utils import Dict, Dictlise


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
                    body = this.request.body
                    this.arguments = Dictlise(json.loads(body))
                except ValueError:
                    this.arguments = Dictlise(self._extract_first_arg(this.request.body_arguments))
            else:
                this.arguments = Dictlise(self._extract_first_arg(this.request.arguments))
        elif this.request.method == 'GET':
            this.arguments = Dictlise(self._extract_first_arg(this.request.query_arguments))


class RequestLog(PrepareExt):

    def __call__(self):
        this = self.handler
        # this.tracker.logging_request_header(this)
        this.tracker.logging_request_body(this)


class ResponseLog(FinishExt):

    def __call__(self):
        this = self.handler
        if this.request.method == "POST":
            this.tracker.logging_response(this)


class CORSExt(ResHandleExt):

    def __call__(self, *args, **kwargs):
        this = self.handler
        this.set_header("Content-Type", "application/jsonx")
        this.set_header("Access-Control-Allow-Origin", "*")
        this.set_header("Access-Control-Allow-Methods", 'GET, POST, OPTIONS')
        this.set_header("Access-Control-Allow-Headers", "DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization")
