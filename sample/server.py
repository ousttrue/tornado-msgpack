#!/usr/bin/env python

import tornado_msgpack


if __name__=="__main__":
    port=18080

    # dispatcher
    dispatcher=tornado_msgpack.Dispatcher()
    def add(a, b):
        return a+b
    dispatcher.add_handler("add", add)

    import tornado
    import threading
    # server
    server_loop=tornado.ioloop.IOLoop()
    server_thread=threading.Thread(target=lambda : server_loop.start())
    server=tornado_msgpack.Server(server_loop, dispatcher.on_message)
    server.listen(port)
    server_thread.start()

