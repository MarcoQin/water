#!/usr/bin/env python
# encoding: utf-8

import os
from tornado import template

from water.utils.common_utils import camel_convert

prefix = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class AutoTemplate(object):

    def __init__(self, template_or_instance):
        self.template = ''
        if isinstance(template_or_instance, basestring):
            tmp = template_or_instance
            if os.path.exists(tmp):
                tmp = os.path.abspath(tmp)
            else:
                tmp = os.path.join(prefix, tmp)
            self.template = tmp
        else:
            ins = template_or_instance
            tmp_path = ins.__module__.replace('.', '/').replace('view', 'static', 1)
            tmp_name = camel_convert(ins.__class__.__name__) + '.html'
            self.template = os.path.join(prefix, tmp_path, tmp_name)

    def get_template(self):
        return self.template

    def render_string(self, **kwargs):
        loader = template.Loader("")
        t = loader.load(self.get_template())
        return t.generate(**kwargs)
