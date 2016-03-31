#!/usr/bin/env python
# encoding: utf-8

import os
from utils.common_utils import camel_convert


class AutoTemplate(object):

    def __init__(self, template_or_instance):
        self.template = ''
        if isinstance(template_or_instance, basestring):
            self.template = template_or_instance
        else:
            ins = template_or_instance
            tmp_path = ins.__module__.replace('.', '/').replace('view', 'static', 1)
            tmp_name = camel_convert(ins.__class__.__name__) + '.html'
            self.template = os.path.join(tmp_path, tmp_name)

    def get_template(self):
        return self.template
