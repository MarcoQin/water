#!/usr/bin/env python
# encoding: utf-8

import os

import tornado.ioloop
import tornado.web

from tornado import httpserver
from tornado.options import define, options


define('port', default=9000, help="run on the given port", type=int)
define('debug', default=True, help="debug mode", type=bool)


class App(tornado.web.Application):

    def __init__(self):
        # tornado application settings
        tornado_settings = dict(gzip=True,
                                debug=options.debug,
                                # static resources config
                                static_url_prefix='/static/',
                                static_path=os.path.join(os.path.dirname(__file__), "static"),)
        #  tornado.web.Application.__init__(self, handlers=handlers, **tornado_settings)
        tornado.web.Application.__init__(self, handlers=[], **tornado_settings)


def main():
    # handle the commmand line parameters
    tornado.options.parse_command_line()
    port = options.port
    _http_server_app = App()
    http_server = httpserver.HTTPServer(_http_server_app)
    http_server.listen(port)
    print "Server start on port: ", port
    print "Address: http://127.0.0.1:%s" % port
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
