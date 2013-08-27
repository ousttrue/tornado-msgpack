#!/usr/bin/env python

port=28080

import tornado_msgpack
dispatcher=tornado_msgpack.Dispatcher()
def add(a, b):
    return a+b
dispatcher.add_handler("add", add)

with tornado_msgpack.ServerLoop("", port, dispatcher.on_message):
    with tornado_msgpack.ClientLoop("localhost", port) as client:
        print(client.call_sync("add", 3, 4))

