#!/usr/bin/env python

import tornado_msgpack
import tornado

port=18080

# dispatcher
dispatcher=tornado_msgpack.Dispatcher()
def add(a, b):
    return a+b
dispatcher.add_handler("add", add)

# server
server_loop=tornado.ioloop.IOLoop()
server=tornado_msgpack.Server(server_loop, dispatcher.on_message)
server.listen(port)

import signal
def handler(signum, frame):
    server_loop.stop()
signal.signal(signal.SIGINT, handler)

# blocking...
try:
    server_loop.start()
except ex as KeyboardInterrupt:
    pass

