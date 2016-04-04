#!/usr/bin/env python
# encoding: utf-8

from utils.common_utils import Dict


class BaseError(object):

    SUCCESS = 0
    ERROR_PARAME_ERROR = 1

    ERROR_MSG = Dict({
        SUCCESS: "ok",
        ERROR_PARAME_ERROR: "params error",
    })


class AutoError(object):

    def __init__(self, error_id, ext_data=None):
        self.errors = Dict()
        if error_id in BaseError.ERROR_MSG:
            self.errors['msg'] = BaseError.ERROR_MSG[error_id]
        if ext_data and isinstance(ext_data, dict):
            self.errors.update(ext_data)

    def build_errors(self):
        return Dict(errors=self.errors)
