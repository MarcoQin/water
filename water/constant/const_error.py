#!/usr/bin/env python
# encoding: utf-8

from utils.common_utils import Dict


class BaseError(object):

    SUCCESS = 0
    ERROR_PARAME_ERROR = 1

    ERROR_MSG = Dict(
        SUCCESS="ok",
        ERROR_PARAME_ERROR="params error",
    )


class AutoError(object):

    def __init__(self, error_id, **kwargs):
        pass
