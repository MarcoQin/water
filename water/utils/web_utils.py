#!/usr/bin/env python
# encoding: utf-8

import requests
# from urlparse import urlparse
from gevent import Timeout


class Redirect(object):

    def __init__(self, url):
        self.url = url

    def do_redirect(self, handler):
        handler.redirect(self.url)


class WebUtils(object):

    # @classmethod
    # def get_domain(cls, url):
        # return urlparse(url).netloc

    @classmethod
    def get_redirect_location(cls, url):
        location = url
        try:
            with Timeout(120):
                r = requests.head(url, allow_redirects=True, timeout=120, verify=False)
                try:
                    location = r.url
                except Exception:
                    location = r.headers.get('location', url)
        except Exception:
            pass
        return location
