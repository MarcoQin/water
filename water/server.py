#!/usr/bin/env python
# encoding: utf-8

import os
import time
import logging
import signal

import tornado.ioloop
import tornado.web

from tornado import httpserver
from tornado.options import define, options

from inits.log_init import init_log
from config.config import MAX_WAIT_SECONDS_BEFORE_SHUTDOWN


define('port', default=9000, help="run on the given port", type=int)
define('debug', default=True, help="debug mode", type=bool)


def close_server():
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        io_loop = tornado.ioloop.IOLoop.instance()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('...Shutdown...')
    stop_loop()
    logging.info("...close_httpserver():ready...")


# handle signal
def server_shutdown_handler(sig, frame):
    logging.warning('...Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(close_server)


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
    init_log(port)

    # added signal callback to interrupt app
    signal.signal(signal.SIGINT, server_shutdown_handler)
    signal.signal(signal.SIGTERM, server_shutdown_handler)

    _http_server_app = App()
    http_server = httpserver.HTTPServer(_http_server_app)
    http_server.listen(port)
    logging.info('...Server started on port: %s...'% port)
    logging.info('...Address: http://127.0.0.1:%s ...'% port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
