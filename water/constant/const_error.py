#!/usr/bin/env python
# encoding: utf-8

from water.utils.common_utils import Dict


class BaseError(object):

    SUCCESS = 0
    ERROR_PARAME_ERROR = 1

    ERROR_MSG = Dict({
        SUCCESS: "ok",
        ERROR_PARAME_ERROR: "params error",
    })


class AutoError(object):

    def __init__(self, error_id, message, ext_data=None):
        self.errors = Dict()
        self.errors['code'] =  error_id
        if error_id in BaseError.ERROR_MSG:
            self.errors['msg'] = BaseError.ERROR_MSG[error_id]
        else:
            self.errors['msg'] = message
        if ext_data and isinstance(ext_data, dict):
            self.errors.update(ext_data)

    def build_errors(self):
        return self.errors
